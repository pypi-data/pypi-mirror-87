# Copyright 2019-2020 Cambridge Quantum Computing
#
# Licensed under a Non-Commercial Use Software Licence (the "Licence");
# you may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and
# limitations under the Licence, but note it is strictly for non-commercial use.

"""Methods to allow conversion between Cirq and t|ket> data types, including Circuits and Devices
"""

from typing import List, Generator, Dict, Union, Iterator
import cirq
from cirq.google import XmonDevice
from cirq import Qid, LineQubit, GridQubit, GlobalPhaseOperation
from cirq.ops import NamedQubit, measure

from pytket.circuit import Circuit, Op, OpType, Qubit, Bit, Node
from pytket.device import Device, QubitErrorContainer
from pytket.routing import Architecture

from sympy import pi, Expr
import cmath
from logging import warning

# For translating cirq circuits to tket circuits
cirq_common = cirq.ops.common_gates
cirq_pauli = cirq.ops.pauli_gates

# map cirq common gates to pytket gates
_cirq2ops_mapping = {
    cirq_common.CNOT: OpType.CX,
    cirq_common.H: OpType.H,
    cirq_common.MeasurementGate: OpType.Measure,
    cirq_common.XPowGate: OpType.Rx,
    cirq_common.YPowGate: OpType.Ry,
    cirq_common.ZPowGate: OpType.Rz,
    cirq_common.S: OpType.S,
    cirq_common.SWAP: OpType.SWAP,
    cirq_common.T: OpType.T,
    cirq_pauli.X: OpType.X,
    cirq_pauli.Y: OpType.Y,
    cirq_pauli.Z: OpType.Z,
    cirq.I: OpType.noop,
    cirq_common.CZPowGate: OpType.CU1,
    cirq_common.CZ: OpType.CZ,
    cirq.CSwapGate: OpType.CSWAP,
    cirq_common.ISwapPowGate: OpType.ISWAP,
    cirq_common.ISWAP: OpType.ISWAPMax,
    cirq.FSimGate: OpType.FSim,
    cirq.google.SYC: OpType.Sycamore,
    cirq.ops.parity_gates.ZZPowGate: OpType.ZZPhase,
    cirq.ops.parity_gates.XXPowGate: OpType.XXPhase,
    cirq.ops.parity_gates.YYPowGate: OpType.YYPhase,
    cirq.ops.PhasedXPowGate: OpType.PhasedX,
    cirq.ops.PhasedISwapPowGate: OpType.PhasedISWAP,
}
# reverse mapping for convenience
_ops2cirq_mapping = dict((reversed(item) for item in _cirq2ops_mapping.items()))
# _ops2cirq_mapping[OpType.X] = cirq_pauli.X
# _ops2cirq_mapping[OpType.Y] = cirq_pauli.Y
# _ops2cirq_mapping[OpType.Z] = cirq_pauli.Z
# spot special rotation gates
_constant_gates = (
    cirq_common.CNOT,
    cirq_common.H,
    cirq_common.S,
    cirq_common.SWAP,
    cirq_common.T,
    cirq_pauli.X,
    cirq_pauli.Y,
    cirq_pauli.Z,
    cirq_common.CZ,
    cirq_common.ISWAP,
    cirq.google.SYC,
    cirq.I,
)
_rotation_types = (
    cirq_common.XPowGate,
    cirq_common.YPowGate,
    cirq_common.ZPowGate,
    cirq_common.CZPowGate,
    cirq_common.ISwapPowGate,
    cirq.ops.parity_gates.ZZPowGate,
    cirq.ops.parity_gates.XXPowGate,
    cirq.ops.parity_gates.YYPowGate,
)


def cirq_to_tk(circuit: cirq.Circuit) -> Circuit:
    """Converts a Cirq :py:class:`Circuit` to a :math:`\\mathrm{t|ket}\\rangle` :py:class:`Circuit` object.

    :param circuit: The input Cirq :py:class:`Circuit`

    :raises NotImplementedError: If the input contains a Cirq :py:class:`Circuit` operation which is not yet supported by pytket

    :return: The :math:`\\mathrm{t|ket}\\rangle` :py:class:`Circuit` corresponding to the input circuit
    """
    tkcirc = Circuit()
    qmap = {}
    for qb in circuit.all_qubits():
        if isinstance(qb, LineQubit):
            id = Qubit("q", qb.x)
        elif isinstance(qb, GridQubit):
            id = Qubit("g", qb.row, qb.col)
        elif isinstance(qb, NamedQubit):
            id = Qubit(qb.name)
        else:
            raise NotImplementedError("Cannot convert qubits of type " + str(type(qb)))
        tkcirc.add_qubit(id)
        qmap.update({qb: id})
    for moment in circuit:
        for op in moment.operations:
            if isinstance(op, GlobalPhaseOperation):
                tkcirc.add_phase(cmath.phase(op.coefficient) / pi)
                continue
            gate = op.gate
            gatetype = type(gate)

            qb_lst = [qmap[q] for q in op.qubits]

            n_qubits = len(op.qubits)

            if gatetype == cirq_common.HPowGate and gate.exponent == 1:
                gate = cirq_common.H
            elif gatetype == cirq_common.CNotPowGate and gate.exponent == 1:
                gate = cirq_common.CNOT
            elif gatetype == cirq_pauli._PauliX and gate.exponent == 1:
                gate = cirq_pauli.X
            elif gatetype == cirq_pauli._PauliY and gate.exponent == 1:
                gate = cirq_pauli.Y
            elif gatetype == cirq_pauli._PauliZ and gate.exponent == 1:
                gate = cirq_pauli.Z

            if gate in _constant_gates:
                try:
                    optype = _cirq2ops_mapping[gate]
                except KeyError as error:
                    raise NotImplementedError(
                        "Operation not supported by tket: " + str(op.gate)
                    ) from error
                params = []
            elif isinstance(gate, cirq_common.MeasurementGate):
                id = Bit(gate.key)
                tkcirc.add_bit(id)
                tkcirc.Measure(*qb_lst, id)
                continue
            elif isinstance(gate, cirq.PhasedXPowGate):
                optype = OpType.PhasedX
                pe = gate.phase_exponent
                e = gate.exponent
                params = [e, pe]
            elif isinstance(gate, cirq.FSimGate):
                optype = OpType.FSim
                params = [gate.theta / pi, gate.phi / pi]
            elif isinstance(gate, cirq.PhasedISwapPowGate):
                optype = OpType.PhasedISWAP
                params = [gate.phase_exponent, gate.exponent]
            else:
                try:
                    optype = _cirq2ops_mapping[gatetype]
                except KeyError as error:
                    raise NotImplementedError(
                        "Operation not supported by tket: " + str(op.gate)
                    ) from error
                params = [gate.exponent]
            tkcirc.add_gate(optype, params, qb_lst)
    return tkcirc


def tk_to_cirq(tkcirc: Circuit) -> cirq.Circuit:
    """Converts a :math:`\\mathrm{t|ket}\\rangle` :py:class:`Circuit` object to a Cirq :py:class:`Circuit`.

    :param tkcirc: The input :math:`\\mathrm{t|ket}\\rangle` :py:class:`Circuit`

    :return: The Cirq :py:class:`Circuit` corresponding to the input circuit
    """
    qmap = {}
    line_name = None
    grid_name = None
    # Since Cirq can only support registers of up to 2 dimensions, we explicitly
    # check for 3-dimensional registers whose third dimension is trivial.
    # SquareGrid architectures are of this form.
    indices = [qb.index for qb in tkcirc.qubits]
    is_flat_3d = all(idx[2] == 0 for idx in indices if len(idx) == 3)
    for qb in tkcirc.qubits:
        if len(qb.index) == 0:
            qmap.update({qb: NamedQubit(qb.reg_name)})
        elif len(qb.index) == 1:
            if line_name and line_name != qb.reg_name:
                raise NotImplementedError(
                    "Cirq can only support a single linear register"
                )
            line_name = qb.reg_name
            qmap.update({qb: LineQubit(qb.index[0])})
        elif len(qb.index) == 2 or (len(qb.index) == 3 and is_flat_3d):
            if grid_name and grid_name != qb.reg_name:
                raise NotImplementedError(
                    "Cirq can only support a single grid register"
                )
            grid_name = qb.reg_name
            qmap.update({qb: GridQubit(qb.index[0], qb.index[1])})
        else:
            raise NotImplementedError(
                "Cirq can only support registers of dimension <=2"
            )
    oplst = []
    for command in tkcirc:
        op = command.op
        optype = op.type
        try:
            gatetype = _ops2cirq_mapping[optype]
        except KeyError as error:
            raise NotImplementedError(
                "Cannot convert tket Op to Cirq gate: " + op.get_name()
            ) from error
        if optype == OpType.Measure:
            qid = qmap[command.args[0]]
            bit = command.args[1]
            cirqop = measure(qid, key=bit.__repr__())
        else:
            qids = [qmap[qbit] for qbit in command.args]
            params = op.params
            if len(params) == 0:
                cirqop = gatetype(*qids)
            elif optype == OpType.PhasedX:
                cirqop = gatetype(phase_exponent=params[1], exponent=params[0])(*qids)
            elif optype == OpType.FSim:
                cirqop = gatetype(
                    theta=float(params[0] * pi), phi=float(params[1] * pi)
                )(*qids)
            elif optype == OpType.PhasedISWAP:
                cirqop = gatetype(phase_exponent=params[0], exponent=params[1])(*qids)
            else:
                cirqop = gatetype(exponent=params[0])(*qids)
        oplst.append(cirqop)

    try:
        coeff = cmath.exp(float(tkcirc.phase) * cmath.pi * 1j)
        if coeff != 1.0:
            oplst.append(GlobalPhaseOperation(coeff))
    except ValueError:
        warning(
            "Global phase is dependent on a symbolic parameter, so cannot adjust for phase"
        )

    return cirq.Circuit(*oplst)


# For converting cirq devices to tket devices


def _sort_row_col(qubits: Iterator[GridQubit]) -> List[GridQubit]:
    """Sort grid qubits first by row then by column"""

    return sorted(qubits, key=lambda x: (x.row, x.col))


def process_characterisation(xmon: XmonDevice) -> dict:
    """Generates a :math:`\\mathrm{t|ket}\\rangle` dictionary containing device characteristics for a Cirq :py:class:`XmonDevice` .

    :param xmon: The device to convert

    :return: A dictionary containing device characteristics
    """
    qb_map = {q: Node("q", q.row, q.col) for q in xmon.qubits}

    indexed_qubits = _sort_row_col(xmon.qubits)
    coupling_map = []
    for qb in indexed_qubits:
        neighbours = xmon.neighbors_of(qb)
        for x in neighbours:
            coupling_map.append((qb_map[qb], qb_map[x]))
    arc = Architecture(coupling_map)

    node_ers_dict = {}
    link_ers_dict = {}

    px_duration = xmon.duration_of(cirq.X(GridQubit(0, 0))).total_nanos()
    cz_duration = xmon.duration_of(
        cirq.CZ(GridQubit(0, 0), GridQubit(0, 1))
    ).total_nanos()
    for qb in xmon.qubits:
        error_cont = QubitErrorContainer({OpType.PhasedX, OpType.Rz})
        error_cont.add_error((OpType.PhasedX, 0.0))
        error_cont.add_error((OpType.Rz, 0.0))
        node_ers_dict[qb_map[qb]] = error_cont

    for a, b in coupling_map:
        error_cont = QubitErrorContainer({OpType.CZ})
        error_cont.add_error((OpType.CZ, 0.0))
        link_ers_dict[(a, b)] = error_cont
        link_ers_dict[(b, a)] = error_cont

    characterisation = dict()
    characterisation["NodeErrors"] = node_ers_dict
    characterisation["EdgeErrors"] = link_ers_dict
    characterisation["Architecture"] = arc

    return characterisation
