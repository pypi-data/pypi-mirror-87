"""A C++ port of the NEO3 Virtual Machine"""
import neo3vm
from pybiginteger import BigInteger
import typing
__all__  = [
"StackItem",
"PrimitiveType",
"BufferStackItem",
"ByteStringStackItem",
"CompoundType",
"EvaluationStack",
"ExceptionHandlingContext",
"ExceptionHandlingState",
"ExecutionContext",
"ExecutionEngine",
"Instruction",
"IntegerStackItem",
"InteropStackItem",
"MapStackItem",
"Neo3vmException",
"NullStackItem",
"OpCode",
"PointerStackItem",
"BooleanStackItem",
"ReferenceCounter",
"Script",
"ScriptBuilder",
"Slot",
"ArrayStackItem",
"StackItemType",
"StructStackItem",
"VMState"
]
class StackItem():
    def convert_to(self, destination_type: StackItemType) -> StackItem: 
        """
        Try to convert the current item to a different stack item type
        """
    def deep_copy(self) -> StackItem: ...
    @staticmethod
    def from_interface(value: object) -> StackItem: 
        """
        Create a stack item (Null or InteropInterface) from any Python object.
        """
    def get_type(self) -> StackItemType: 
        """
        Get the stack item type
        """
    def to_array(self) -> bytes: ...
    def to_biginteger(self) -> BigInteger: ...
    def to_boolean(self) -> bool: ...
    pass
class PrimitiveType(StackItem):
    def __len__(self) -> int: ...
    def to_array(self) -> bytes: 
        """
        Return the underlying data as a bytes
        """
    pass
class BufferStackItem(StackItem):
    @typing.overload
    def __init__(self, data: bytes) -> None: 
        """
        Create a buffer with an initial size

        Create a buffer from binary data
        """
    @typing.overload
    def __init__(self, size: int) -> None: ...
    def __len__(self) -> int: ...
    def __str__(self) -> str: ...
    def to_array(self) -> bytes: ...
    pass
class ByteStringStackItem(PrimitiveType, StackItem):
    def __eq__(self, arg0: StackItem) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, value: bytes) -> None: ...
    @typing.overload
    def __init__(self, value: str) -> None: ...
    def __len__(self) -> int: ...
    def __str__(self) -> str: ...
    pass
class CompoundType(StackItem):
    pass
class EvaluationStack():
    def __init__(self, reference_counter: ReferenceCounter) -> None: ...
    def __len__(self) -> int: ...
    def clear(self) -> None: 
        """
        Remove all internal items.
        """
    def insert(self, index: int, item: StackItem) -> None: 
        """
        Add an item at a specific index
        """
    def peek(self, index: int = 0) -> StackItem: 
        """
        Return the top item or if specific the item at the given index.
        """
    def pop(self) -> StackItem: 
        """
        Remove and return the top item from the stack
        """
    def push(self, item: StackItem) -> None: 
        """
        Push item onto the stack
        """
    def remove(self, index: int) -> StackItem: 
        """
        Remove and return the item at the given index
        """
    @property
    def _items(self) -> typing.List[StackItem]:
        """
        :type: typing.List[StackItem]
        """
    pass
class ExceptionHandlingContext():
    def __init__(self, catch_pointer: int, finally_pointer: int) -> None: ...
    def has_catch(self) -> bool: ...
    def has_finally(self) -> bool: ...
    @property
    def catch_pointer(self) -> int:
        """
        :type: int
        """
    @catch_pointer.setter
    def catch_pointer(self, arg0: int) -> None:
        pass
    @property
    def end_pointer(self) -> int:
        """
        :type: int
        """
    @end_pointer.setter
    def end_pointer(self, arg0: int) -> None:
        pass
    @property
    def finally_pointer(self) -> int:
        """
        :type: int
        """
    @finally_pointer.setter
    def finally_pointer(self, arg0: int) -> None:
        pass
    @property
    def state(self) -> ExceptionHandlingState:
        """
        :type: ExceptionHandlingState
        """
    @state.setter
    def state(self, arg0: ExceptionHandlingState) -> None:
        pass
    pass
class ExceptionHandlingState():
    """
    Members:

      TRY

      CATCH

      FINALLY
    """
    def __index__(self) -> int: ...
    def __init__(self, arg0: int) -> None: ...
    def __int_(self) -> int: ...
    @property
    def name(self) -> str:
        """
        (self: handle) -> str

        :type: str
        """
    CATCH: neo3vm.ExceptionHandlingState # value = ExceptionHandlingState.CATCH
    FINALLY: neo3vm.ExceptionHandlingState # value = ExceptionHandlingState.FINALLY
    TRY: neo3vm.ExceptionHandlingState # value = ExceptionHandlingState.TRY
    __members__: dict # value = {'TRY': ExceptionHandlingState.TRY, 'CATCH': ExceptionHandlingState.CATCH, 'FINALLY': ExceptionHandlingState.FINALLY}
    pass
class ExecutionContext():
    def __init__(self, script: Script, reference_counter: ReferenceCounter) -> None: ...
    def current_instruction(self) -> Instruction: ...
    @property
    def arguments(self) -> Slot:
        """
        :type: Slot
        """
    @property
    def call_flags(self) -> int:
        """
        :type: int
        """
    @call_flags.setter
    def call_flags(self, arg0: int) -> None:
        pass
    @property
    def calling_script(self) -> Script:
        """
        :type: Script
        """
    @calling_script.setter
    def calling_script(self, arg0: Script) -> None:
        pass
    @property
    def evaluation_stack(self) -> EvaluationStack:
        """
        :type: EvaluationStack
        """
    @property
    def ip(self) -> int:
        """
        Instruction pointer

        :type: int
        """
    @ip.setter
    def ip(self, arg0: int) -> None:
        """
        Instruction pointer
        """
    @property
    def local_variables(self) -> Slot:
        """
        :type: Slot
        """
    @property
    def script(self) -> Script:
        """
        :type: Script
        """
    @script.setter
    def script(self, arg0: Script) -> None:
        pass
    @property
    def static_fields(self) -> Slot:
        """
        :type: Slot
        """
    @property
    def try_stack(self) -> typing.List[ExceptionHandlingContext]:
        """
        :type: typing.List[ExceptionHandlingContext]
        """
    pass
class ExecutionEngine():
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, reference_counter: ReferenceCounter) -> None: ...
    def _execute_next(self) -> None: ...
    def context_unloaded(self, arg0: ExecutionContext) -> None: ...
    def execute(self) -> VMState: ...
    def load_cloned_context(self, arg0: int) -> None: ...
    def load_context(self, arg0: ExecutionContext) -> None: ...
    def load_script(self, script: Script, initial_position: int = 0) -> ExecutionContext: 
        """
        Load script into engine
        """
    def on_syscall(self, method_id: int) -> None: ...
    def pop(self) -> StackItem: 
        """
        Pop the top item from the evaluation stack of the current context.
        """
    def pop_bool(self) -> bool: ...
    def pop_bytes(self) -> bytes: ...
    def pop_int(self) -> BigInteger: ...
    def post_execute_instruction(self, arg0: Instruction) -> None: ...
    def pre_execute_instruction(self) -> None: ...
    def push(self, stack_item: StackItem) -> None: 
        """
        Push an item onto the evaluation stack of the current context.
        """
    def throw(self, exception_stack_item: StackItem) -> None: 
        """
        Use to throw exceptions from SYSCALLs
        """
    @property
    def current_context(self) -> ExecutionContext:
        """
        :type: ExecutionContext
        """
    @property
    def entry_context(self) -> ExecutionContext:
        """
        :type: ExecutionContext
        """
    @property
    def exception_message(self) -> str:
        """
        :type: str
        """
    @property
    def instruction_counter(self) -> int:
        """
        Instruction counter

        :type: int
        """
    @property
    def invocation_stack(self) -> typing.List[ExecutionContext]:
        """
        :type: typing.List[ExecutionContext]
        """
    @property
    def reference_counter(self) -> ReferenceCounter:
        """
        :type: ReferenceCounter
        """
    @property
    def result_stack(self) -> EvaluationStack:
        """
        :type: EvaluationStack
        """
    @property
    def state(self) -> VMState:
        """
        :type: VMState
        """
    @state.setter
    def state(self, arg0: VMState) -> None:
        pass
    @property
    def uncaught_exception(self) -> StackItem:
        """
        :type: StackItem
        """
    MAX_INVOCATION_STACK_SIZE = 1024
    MAX_ITEM_SIZE = 1048576
    MAX_SHIFT = 256
    MAX_STACK_SIZE = 2048
    pass
class Instruction():
    @staticmethod
    def RET() -> Instruction: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, script: bytes, ip: int) -> None: ...
    def __len__(self) -> int: ...
    def __str__(self) -> str: ...
    @property
    def opcode(self) -> OpCode:
        """
        :type: OpCode
        """
    @property
    def operand(self) -> bytes:
        """
        :type: bytes
        """
    @property
    def token_16(self) -> bytes:
        """
        :type: bytes
        """
    @property
    def token_32(self) -> bytes:
        """
        :type: bytes
        """
    @property
    def token_8(self) -> bytes:
        """
        :type: bytes
        """
    @property
    def token_8_1(self) -> bytes:
        """
        :type: bytes
        """
    @property
    def token_i16(self) -> int:
        """
        :type: int
        """
    @property
    def token_i32(self) -> int:
        """
        :type: int
        """
    @property
    def token_i32_1(self) -> int:
        """
        :type: int
        """
    @property
    def token_i8(self) -> int:
        """
        :type: int
        """
    @property
    def token_i8_1(self) -> int:
        """
        :type: int
        """
    @property
    def token_string(self) -> str:
        """
        :type: str
        """
    @property
    def token_u16(self) -> int:
        """
        :type: int
        """
    @property
    def token_u32(self) -> int:
        """
        :type: int
        """
    @property
    def token_u8(self) -> int:
        """
        :type: int
        """
    @property
    def token_u8_1(self) -> int:
        """
        :type: int
        """
    pass
class IntegerStackItem(PrimitiveType, StackItem):
    def __eq__(self, arg0: StackItem) -> bool: ...
    @typing.overload
    def __init__(self, data: bytes) -> None: ...
    @typing.overload
    def __init__(self, value: BigInteger) -> None: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    def __int_(self) -> int: ...
    def __len__(self) -> int: ...
    def __str__(self) -> str: ...
    MAX_SIZE = 32
    pass
class InteropStackItem(StackItem):
    def __eq__(self, arg0: StackItem) -> bool: ...
    def __init__(self, object_instance: object) -> None: ...
    def __str__(self) -> object: ...
    def get_object(self) -> object: 
        """
        Get the internally stored object
        """
    pass
class MapStackItem(CompoundType, StackItem):
    def __contains__(self, arg0: PrimitiveType) -> bool: ...
    def __getitem__(self, arg0: PrimitiveType) -> StackItem: ...
    def __init__(self, reference_counter: ReferenceCounter) -> None: 
        """
        Warning: make sure the reference counter passed in outlives this object.
                    Note: This means that creating the reference counter inside the constructor can cause it to be cleaned up by Python before this object's life ended
        """
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __reversed__(self) -> typing.Iterator: ...
    def __setitem__(self, arg0: PrimitiveType, arg1: StackItem) -> None: ...
    def clear(self) -> None: 
        """
        Remove all internal items.
        """
    def keys(self) -> typing.List[StackItem]: ...
    def remove(self, key: PrimitiveType) -> None: 
        """
        Remove pair by key
        """
    def values(self) -> typing.List[StackItem]: ...
    pass
class Neo3vmException(Exception, BaseException):
    pass
class NullStackItem(StackItem):
    def __eq__(self, arg0: StackItem) -> bool: ...
    def __init__(self) -> None: ...
    pass
class OpCode():
    """
    Members:

      PUSHDATA1

      PUSHDATA2

      PUSHDATA4

      PUSHINT8

      PUSHINT16

      PUSHINT32

      PUSHINT64

      PUSHINT128

      PUSHINT256

      INITSSLOT

      INITSLOT

      RET

      NOP

      PUSHM1

      PUSH0

      PUSH1

      PUSH2

      PUSH3

      PUSH4

      PUSH5

      PUSH6

      PUSH7

      PUSH8

      PUSH9

      PUSH10

      PUSH11

      PUSH12

      PUSH13

      PUSH14

      PUSH15

      PUSH16

      PUSHNULL

      PUSHA

      THROW

      TRY

      TRY_L

      ENDTRY

      ENDTRY_L

      ENDFINALLY

      ASSERT

      ABORT

      JMP

      JMP_L

      JMPIF

      JMPIF_L

      JMPIFNOT

      JMPIFNOT_L

      JMPEQ

      JMPEQ_L

      JMPNE

      JMPNE_L

      JMPGT

      JMPGT_L

      JMPGE

      JMPGE_L

      JMPLT

      JMPLT_L

      JMPLE

      JMPLE_L

      CALL

      CALL_L

      CALLA

      DEPTH

      DROP

      NIP

      XDROP

      CLEAR

      DUP

      OVER

      PICK

      TUCK

      SWAP

      ROT

      ROLL

      NEWMAP

      REVERSE3

      REVERSE4

      REVERSEN

      STSFLD0

      STSFLD1

      STSFLD2

      STSFLD3

      STSFLD4

      STSFLD5

      STSFLD6

      STSFLD

      LDSFLD0

      LDSFLD1

      LDSFLD2

      LDSFLD3

      LDSFLD4

      LDSFLD5

      LDSFLD6

      LDSFLD

      STLOC0

      STLOC1

      STLOC2

      STLOC3

      STLOC4

      STLOC5

      STLOC6

      STLOC

      LDLOC0

      LDLOC1

      LDLOC2

      LDLOC3

      LDLOC4

      LDLOC5

      LDLOC6

      LDLOC

      STARG0

      STARG1

      STARG2

      STARG3

      STARG4

      STARG5

      STARG6

      STARG

      LDARG0

      LDARG1

      LDARG2

      LDARG3

      LDARG4

      LDARG5

      LDARG6

      LDARG

      NEWBUFFER

      NEWARRAY

      MEMCPY

      CAT

      DEC

      CONVERT

      SUBSTR

      LEFT

      RIGHT

      INVERT

      NEWSTRUCT

      AND

      OR

      XOR

      EQUAL

      NOTEQUAL

      SIGN

      ABS

      NEGATE

      INC

      ADD

      SUB

      MUL

      DIV

      MOD

      SHL

      SHR

      NOT

      BOOLAND

      BOOLOR

      NZ

      NUMEQUAL

      NUMNOTEQUAL

      LT

      LE

      GT

      GE

      MIN

      MAX

      WITHIN

      PACK

      UNPACK

      NEWARRAY0

      NEWARRAY_T

      SETITEM

      NEWSTRUCT0

      SIZE

      HASKEY

      KEYS

      VALUES

      PICKITEM

      APPEND

      REVERSEITEMS

      REMOVE

      CLEARITEMS

      ISNULL

      ISTYPE

      SYSCALL
    """
    def __index__(self) -> int: ...
    def __init__(self, arg0: int) -> None: ...
    def __int_(self) -> int: ...
    @property
    def name(self) -> str:
        """
        (self: handle) -> str

        :type: str
        """
    ABORT: neo3vm.OpCode # value = OpCode.ABORT
    ABS: neo3vm.OpCode # value = OpCode.ABS
    ADD: neo3vm.OpCode # value = OpCode.ADD
    AND: neo3vm.OpCode # value = OpCode.AND
    APPEND: neo3vm.OpCode # value = OpCode.APPEND
    ASSERT: neo3vm.OpCode # value = OpCode.ASSERT
    BOOLAND: neo3vm.OpCode # value = OpCode.BOOLAND
    BOOLOR: neo3vm.OpCode # value = OpCode.BOOLOR
    CALL: neo3vm.OpCode # value = OpCode.CALL
    CALLA: neo3vm.OpCode # value = OpCode.CALLA
    CALL_L: neo3vm.OpCode # value = OpCode.CALL_L
    CAT: neo3vm.OpCode # value = OpCode.CAT
    CLEAR: neo3vm.OpCode # value = OpCode.CLEAR
    CLEARITEMS: neo3vm.OpCode # value = OpCode.CLEARITEMS
    CONVERT: neo3vm.OpCode # value = OpCode.CONVERT
    DEC: neo3vm.OpCode # value = OpCode.DEC
    DEPTH: neo3vm.OpCode # value = OpCode.DEPTH
    DIV: neo3vm.OpCode # value = OpCode.DIV
    DROP: neo3vm.OpCode # value = OpCode.DROP
    DUP: neo3vm.OpCode # value = OpCode.DUP
    ENDFINALLY: neo3vm.OpCode # value = OpCode.ENDFINALLY
    ENDTRY: neo3vm.OpCode # value = OpCode.ENDTRY
    ENDTRY_L: neo3vm.OpCode # value = OpCode.ENDTRY_L
    EQUAL: neo3vm.OpCode # value = OpCode.EQUAL
    GE: neo3vm.OpCode # value = OpCode.GE
    GT: neo3vm.OpCode # value = OpCode.GT
    HASKEY: neo3vm.OpCode # value = OpCode.HASKEY
    INC: neo3vm.OpCode # value = OpCode.INC
    INITSLOT: neo3vm.OpCode # value = OpCode.INITSLOT
    INITSSLOT: neo3vm.OpCode # value = OpCode.INITSSLOT
    INVERT: neo3vm.OpCode # value = OpCode.INVERT
    ISNULL: neo3vm.OpCode # value = OpCode.ISNULL
    ISTYPE: neo3vm.OpCode # value = OpCode.ISTYPE
    JMP: neo3vm.OpCode # value = OpCode.JMP
    JMPEQ: neo3vm.OpCode # value = OpCode.JMPEQ
    JMPEQ_L: neo3vm.OpCode # value = OpCode.JMPEQ_L
    JMPGE: neo3vm.OpCode # value = OpCode.JMPGE
    JMPGE_L: neo3vm.OpCode # value = OpCode.JMPGE_L
    JMPGT: neo3vm.OpCode # value = OpCode.JMPGT
    JMPGT_L: neo3vm.OpCode # value = OpCode.JMPGT_L
    JMPIF: neo3vm.OpCode # value = OpCode.JMPIF
    JMPIFNOT: neo3vm.OpCode # value = OpCode.JMPIFNOT
    JMPIFNOT_L: neo3vm.OpCode # value = OpCode.JMPIFNOT_L
    JMPIF_L: neo3vm.OpCode # value = OpCode.JMPIF_L
    JMPLE: neo3vm.OpCode # value = OpCode.JMPLE
    JMPLE_L: neo3vm.OpCode # value = OpCode.JMPLE_L
    JMPLT: neo3vm.OpCode # value = OpCode.JMPLT
    JMPLT_L: neo3vm.OpCode # value = OpCode.JMPLT_L
    JMPNE: neo3vm.OpCode # value = OpCode.JMPNE
    JMPNE_L: neo3vm.OpCode # value = OpCode.JMPNE_L
    JMP_L: neo3vm.OpCode # value = OpCode.JMP_L
    KEYS: neo3vm.OpCode # value = OpCode.KEYS
    LDARG: neo3vm.OpCode # value = OpCode.LDARG
    LDARG0: neo3vm.OpCode # value = OpCode.LDARG0
    LDARG1: neo3vm.OpCode # value = OpCode.LDARG1
    LDARG2: neo3vm.OpCode # value = OpCode.LDARG2
    LDARG3: neo3vm.OpCode # value = OpCode.LDARG3
    LDARG4: neo3vm.OpCode # value = OpCode.LDARG4
    LDARG5: neo3vm.OpCode # value = OpCode.LDARG5
    LDARG6: neo3vm.OpCode # value = OpCode.LDARG6
    LDLOC: neo3vm.OpCode # value = OpCode.LDLOC
    LDLOC0: neo3vm.OpCode # value = OpCode.LDLOC0
    LDLOC1: neo3vm.OpCode # value = OpCode.LDLOC1
    LDLOC2: neo3vm.OpCode # value = OpCode.LDLOC2
    LDLOC3: neo3vm.OpCode # value = OpCode.LDLOC3
    LDLOC4: neo3vm.OpCode # value = OpCode.LDLOC4
    LDLOC5: neo3vm.OpCode # value = OpCode.LDLOC5
    LDLOC6: neo3vm.OpCode # value = OpCode.LDLOC6
    LDSFLD: neo3vm.OpCode # value = OpCode.LDSFLD
    LDSFLD0: neo3vm.OpCode # value = OpCode.LDSFLD0
    LDSFLD1: neo3vm.OpCode # value = OpCode.LDSFLD1
    LDSFLD2: neo3vm.OpCode # value = OpCode.LDSFLD2
    LDSFLD3: neo3vm.OpCode # value = OpCode.LDSFLD3
    LDSFLD4: neo3vm.OpCode # value = OpCode.LDSFLD4
    LDSFLD5: neo3vm.OpCode # value = OpCode.LDSFLD5
    LDSFLD6: neo3vm.OpCode # value = OpCode.LDSFLD6
    LE: neo3vm.OpCode # value = OpCode.LE
    LEFT: neo3vm.OpCode # value = OpCode.LEFT
    LT: neo3vm.OpCode # value = OpCode.LT
    MAX: neo3vm.OpCode # value = OpCode.MAX
    MEMCPY: neo3vm.OpCode # value = OpCode.MEMCPY
    MIN: neo3vm.OpCode # value = OpCode.MIN
    MOD: neo3vm.OpCode # value = OpCode.MOD
    MUL: neo3vm.OpCode # value = OpCode.MUL
    NEGATE: neo3vm.OpCode # value = OpCode.NEGATE
    NEWARRAY: neo3vm.OpCode # value = OpCode.NEWARRAY
    NEWARRAY0: neo3vm.OpCode # value = OpCode.NEWARRAY0
    NEWARRAY_T: neo3vm.OpCode # value = OpCode.NEWARRAY_T
    NEWBUFFER: neo3vm.OpCode # value = OpCode.NEWBUFFER
    NEWMAP: neo3vm.OpCode # value = OpCode.NEWMAP
    NEWSTRUCT: neo3vm.OpCode # value = OpCode.NEWSTRUCT
    NEWSTRUCT0: neo3vm.OpCode # value = OpCode.NEWSTRUCT0
    NIP: neo3vm.OpCode # value = OpCode.NIP
    NOP: neo3vm.OpCode # value = OpCode.NOP
    NOT: neo3vm.OpCode # value = OpCode.NOT
    NOTEQUAL: neo3vm.OpCode # value = OpCode.NOTEQUAL
    NUMEQUAL: neo3vm.OpCode # value = OpCode.NUMEQUAL
    NUMNOTEQUAL: neo3vm.OpCode # value = OpCode.NUMNOTEQUAL
    NZ: neo3vm.OpCode # value = OpCode.NZ
    OR: neo3vm.OpCode # value = OpCode.OR
    OVER: neo3vm.OpCode # value = OpCode.OVER
    PACK: neo3vm.OpCode # value = OpCode.PACK
    PICK: neo3vm.OpCode # value = OpCode.PICK
    PICKITEM: neo3vm.OpCode # value = OpCode.PICKITEM
    PUSH0: neo3vm.OpCode # value = OpCode.PUSH0
    PUSH1: neo3vm.OpCode # value = OpCode.PUSH1
    PUSH10: neo3vm.OpCode # value = OpCode.PUSH10
    PUSH11: neo3vm.OpCode # value = OpCode.PUSH11
    PUSH12: neo3vm.OpCode # value = OpCode.PUSH12
    PUSH13: neo3vm.OpCode # value = OpCode.PUSH13
    PUSH14: neo3vm.OpCode # value = OpCode.PUSH14
    PUSH15: neo3vm.OpCode # value = OpCode.PUSH15
    PUSH16: neo3vm.OpCode # value = OpCode.PUSH16
    PUSH2: neo3vm.OpCode # value = OpCode.PUSH2
    PUSH3: neo3vm.OpCode # value = OpCode.PUSH3
    PUSH4: neo3vm.OpCode # value = OpCode.PUSH4
    PUSH5: neo3vm.OpCode # value = OpCode.PUSH5
    PUSH6: neo3vm.OpCode # value = OpCode.PUSH6
    PUSH7: neo3vm.OpCode # value = OpCode.PUSH7
    PUSH8: neo3vm.OpCode # value = OpCode.PUSH8
    PUSH9: neo3vm.OpCode # value = OpCode.PUSH9
    PUSHA: neo3vm.OpCode # value = OpCode.PUSHA
    PUSHDATA1: neo3vm.OpCode # value = OpCode.PUSHDATA1
    PUSHDATA2: neo3vm.OpCode # value = OpCode.PUSHDATA2
    PUSHDATA4: neo3vm.OpCode # value = OpCode.PUSHDATA4
    PUSHINT128: neo3vm.OpCode # value = OpCode.PUSHINT128
    PUSHINT16: neo3vm.OpCode # value = OpCode.PUSHINT16
    PUSHINT256: neo3vm.OpCode # value = OpCode.PUSHINT256
    PUSHINT32: neo3vm.OpCode # value = OpCode.PUSHINT32
    PUSHINT64: neo3vm.OpCode # value = OpCode.PUSHINT64
    PUSHINT8: neo3vm.OpCode # value = OpCode.PUSHINT8
    PUSHM1: neo3vm.OpCode # value = OpCode.PUSHM1
    PUSHNULL: neo3vm.OpCode # value = OpCode.PUSHNULL
    REMOVE: neo3vm.OpCode # value = OpCode.REMOVE
    RET: neo3vm.OpCode # value = OpCode.RET
    REVERSE3: neo3vm.OpCode # value = OpCode.REVERSE3
    REVERSE4: neo3vm.OpCode # value = OpCode.REVERSE4
    REVERSEITEMS: neo3vm.OpCode # value = OpCode.REVERSEITEMS
    REVERSEN: neo3vm.OpCode # value = OpCode.REVERSEN
    RIGHT: neo3vm.OpCode # value = OpCode.RIGHT
    ROLL: neo3vm.OpCode # value = OpCode.ROLL
    ROT: neo3vm.OpCode # value = OpCode.ROT
    SETITEM: neo3vm.OpCode # value = OpCode.SETITEM
    SHL: neo3vm.OpCode # value = OpCode.SHL
    SHR: neo3vm.OpCode # value = OpCode.SHR
    SIGN: neo3vm.OpCode # value = OpCode.SIGN
    SIZE: neo3vm.OpCode # value = OpCode.SIZE
    STARG: neo3vm.OpCode # value = OpCode.STARG
    STARG0: neo3vm.OpCode # value = OpCode.STARG0
    STARG1: neo3vm.OpCode # value = OpCode.STARG1
    STARG2: neo3vm.OpCode # value = OpCode.STARG2
    STARG3: neo3vm.OpCode # value = OpCode.STARG3
    STARG4: neo3vm.OpCode # value = OpCode.STARG4
    STARG5: neo3vm.OpCode # value = OpCode.STARG5
    STARG6: neo3vm.OpCode # value = OpCode.STARG6
    STLOC: neo3vm.OpCode # value = OpCode.STLOC
    STLOC0: neo3vm.OpCode # value = OpCode.STLOC0
    STLOC1: neo3vm.OpCode # value = OpCode.STLOC1
    STLOC2: neo3vm.OpCode # value = OpCode.STLOC2
    STLOC3: neo3vm.OpCode # value = OpCode.STLOC3
    STLOC4: neo3vm.OpCode # value = OpCode.STLOC4
    STLOC5: neo3vm.OpCode # value = OpCode.STLOC5
    STLOC6: neo3vm.OpCode # value = OpCode.STLOC6
    STSFLD: neo3vm.OpCode # value = OpCode.STSFLD
    STSFLD0: neo3vm.OpCode # value = OpCode.STSFLD0
    STSFLD1: neo3vm.OpCode # value = OpCode.STSFLD1
    STSFLD2: neo3vm.OpCode # value = OpCode.STSFLD2
    STSFLD3: neo3vm.OpCode # value = OpCode.STSFLD3
    STSFLD4: neo3vm.OpCode # value = OpCode.STSFLD4
    STSFLD5: neo3vm.OpCode # value = OpCode.STSFLD5
    STSFLD6: neo3vm.OpCode # value = OpCode.STSFLD6
    SUB: neo3vm.OpCode # value = OpCode.SUB
    SUBSTR: neo3vm.OpCode # value = OpCode.SUBSTR
    SWAP: neo3vm.OpCode # value = OpCode.SWAP
    SYSCALL: neo3vm.OpCode # value = OpCode.SYSCALL
    THROW: neo3vm.OpCode # value = OpCode.THROW
    TRY: neo3vm.OpCode # value = OpCode.TRY
    TRY_L: neo3vm.OpCode # value = OpCode.TRY_L
    TUCK: neo3vm.OpCode # value = OpCode.TUCK
    UNPACK: neo3vm.OpCode # value = OpCode.UNPACK
    VALUES: neo3vm.OpCode # value = OpCode.VALUES
    WITHIN: neo3vm.OpCode # value = OpCode.WITHIN
    XDROP: neo3vm.OpCode # value = OpCode.XDROP
    XOR: neo3vm.OpCode # value = OpCode.XOR
    __members__: dict # value = {'PUSHDATA1': OpCode.PUSHDATA1, 'PUSHDATA2': OpCode.PUSHDATA2, 'PUSHDATA4': OpCode.PUSHDATA4, 'PUSHINT8': OpCode.PUSHINT8, 'PUSHINT16': OpCode.PUSHINT16, 'PUSHINT32': OpCode.PUSHINT32, 'PUSHINT64': OpCode.PUSHINT64, 'PUSHINT128': OpCode.PUSHINT128, 'PUSHINT256': OpCode.PUSHINT256, 'INITSSLOT': OpCode.INITSSLOT, 'INITSLOT': OpCode.INITSLOT, 'RET': OpCode.RET, 'NOP': OpCode.NOP, 'PUSHM1': OpCode.PUSHM1, 'PUSH0': OpCode.PUSH0, 'PUSH1': OpCode.PUSH1, 'PUSH2': OpCode.PUSH2, 'PUSH3': OpCode.PUSH3, 'PUSH4': OpCode.PUSH4, 'PUSH5': OpCode.PUSH5, 'PUSH6': OpCode.PUSH6, 'PUSH7': OpCode.PUSH7, 'PUSH8': OpCode.PUSH8, 'PUSH9': OpCode.PUSH9, 'PUSH10': OpCode.PUSH10, 'PUSH11': OpCode.PUSH11, 'PUSH12': OpCode.PUSH12, 'PUSH13': OpCode.PUSH13, 'PUSH14': OpCode.PUSH14, 'PUSH15': OpCode.PUSH15, 'PUSH16': OpCode.PUSH16, 'PUSHNULL': OpCode.PUSHNULL, 'PUSHA': OpCode.PUSHA, 'THROW': OpCode.THROW, 'TRY': OpCode.TRY, 'TRY_L': OpCode.TRY_L, 'ENDTRY': OpCode.ENDTRY, 'ENDTRY_L': OpCode.ENDTRY_L, 'ENDFINALLY': OpCode.ENDFINALLY, 'ASSERT': OpCode.ASSERT, 'ABORT': OpCode.ABORT, 'JMP': OpCode.JMP, 'JMP_L': OpCode.JMP_L, 'JMPIF': OpCode.JMPIF, 'JMPIF_L': OpCode.JMPIF_L, 'JMPIFNOT': OpCode.JMPIFNOT, 'JMPIFNOT_L': OpCode.JMPIFNOT_L, 'JMPEQ': OpCode.JMPEQ, 'JMPEQ_L': OpCode.JMPEQ_L, 'JMPNE': OpCode.JMPNE, 'JMPNE_L': OpCode.JMPNE_L, 'JMPGT': OpCode.JMPGT, 'JMPGT_L': OpCode.JMPGT_L, 'JMPGE': OpCode.JMPGE, 'JMPGE_L': OpCode.JMPGE_L, 'JMPLT': OpCode.JMPLT, 'JMPLT_L': OpCode.JMPLT_L, 'JMPLE': OpCode.JMPLE, 'JMPLE_L': OpCode.JMPLE_L, 'CALL': OpCode.CALL, 'CALL_L': OpCode.CALL_L, 'CALLA': OpCode.CALLA, 'DEPTH': OpCode.DEPTH, 'DROP': OpCode.DROP, 'NIP': OpCode.NIP, 'XDROP': OpCode.XDROP, 'CLEAR': OpCode.CLEAR, 'DUP': OpCode.DUP, 'OVER': OpCode.OVER, 'PICK': OpCode.PICK, 'TUCK': OpCode.TUCK, 'SWAP': OpCode.SWAP, 'ROT': OpCode.ROT, 'ROLL': OpCode.ROLL, 'NEWMAP': OpCode.NEWMAP, 'REVERSE3': OpCode.REVERSE3, 'REVERSE4': OpCode.REVERSE4, 'REVERSEN': OpCode.REVERSEN, 'STSFLD0': OpCode.STSFLD0, 'STSFLD1': OpCode.STSFLD1, 'STSFLD2': OpCode.STSFLD2, 'STSFLD3': OpCode.STSFLD3, 'STSFLD4': OpCode.STSFLD4, 'STSFLD5': OpCode.STSFLD5, 'STSFLD6': OpCode.STSFLD6, 'STSFLD': OpCode.STSFLD, 'LDSFLD0': OpCode.LDSFLD0, 'LDSFLD1': OpCode.LDSFLD1, 'LDSFLD2': OpCode.LDSFLD2, 'LDSFLD3': OpCode.LDSFLD3, 'LDSFLD4': OpCode.LDSFLD4, 'LDSFLD5': OpCode.LDSFLD5, 'LDSFLD6': OpCode.LDSFLD6, 'LDSFLD': OpCode.LDSFLD, 'STLOC0': OpCode.STLOC0, 'STLOC1': OpCode.STLOC1, 'STLOC2': OpCode.STLOC2, 'STLOC3': OpCode.STLOC3, 'STLOC4': OpCode.STLOC4, 'STLOC5': OpCode.STLOC5, 'STLOC6': OpCode.STLOC6, 'STLOC': OpCode.STLOC, 'LDLOC0': OpCode.LDLOC0, 'LDLOC1': OpCode.LDLOC1, 'LDLOC2': OpCode.LDLOC2, 'LDLOC3': OpCode.LDLOC3, 'LDLOC4': OpCode.LDLOC4, 'LDLOC5': OpCode.LDLOC5, 'LDLOC6': OpCode.LDLOC6, 'LDLOC': OpCode.LDLOC, 'STARG0': OpCode.STARG0, 'STARG1': OpCode.STARG1, 'STARG2': OpCode.STARG2, 'STARG3': OpCode.STARG3, 'STARG4': OpCode.STARG4, 'STARG5': OpCode.STARG5, 'STARG6': OpCode.STARG6, 'STARG': OpCode.STARG, 'LDARG0': OpCode.LDARG0, 'LDARG1': OpCode.LDARG1, 'LDARG2': OpCode.LDARG2, 'LDARG3': OpCode.LDARG3, 'LDARG4': OpCode.LDARG4, 'LDARG5': OpCode.LDARG5, 'LDARG6': OpCode.LDARG6, 'LDARG': OpCode.LDARG, 'NEWBUFFER': OpCode.NEWBUFFER, 'NEWARRAY': OpCode.NEWARRAY, 'MEMCPY': OpCode.MEMCPY, 'CAT': OpCode.CAT, 'DEC': OpCode.DEC, 'CONVERT': OpCode.CONVERT, 'SUBSTR': OpCode.SUBSTR, 'LEFT': OpCode.LEFT, 'RIGHT': OpCode.RIGHT, 'INVERT': OpCode.INVERT, 'NEWSTRUCT': OpCode.NEWSTRUCT, 'AND': OpCode.AND, 'OR': OpCode.OR, 'XOR': OpCode.XOR, 'EQUAL': OpCode.EQUAL, 'NOTEQUAL': OpCode.NOTEQUAL, 'SIGN': OpCode.SIGN, 'ABS': OpCode.ABS, 'NEGATE': OpCode.NEGATE, 'INC': OpCode.INC, 'ADD': OpCode.ADD, 'SUB': OpCode.SUB, 'MUL': OpCode.MUL, 'DIV': OpCode.DIV, 'MOD': OpCode.MOD, 'SHL': OpCode.SHL, 'SHR': OpCode.SHR, 'NOT': OpCode.NOT, 'BOOLAND': OpCode.BOOLAND, 'BOOLOR': OpCode.BOOLOR, 'NZ': OpCode.NZ, 'NUMEQUAL': OpCode.NUMEQUAL, 'NUMNOTEQUAL': OpCode.NUMNOTEQUAL, 'LT': OpCode.LT, 'LE': OpCode.LE, 'GT': OpCode.GT, 'GE': OpCode.GE, 'MIN': OpCode.MIN, 'MAX': OpCode.MAX, 'WITHIN': OpCode.WITHIN, 'PACK': OpCode.PACK, 'UNPACK': OpCode.UNPACK, 'NEWARRAY0': OpCode.NEWARRAY0, 'NEWARRAY_T': OpCode.NEWARRAY_T, 'SETITEM': OpCode.SETITEM, 'NEWSTRUCT0': OpCode.NEWSTRUCT0, 'SIZE': OpCode.SIZE, 'HASKEY': OpCode.HASKEY, 'KEYS': OpCode.KEYS, 'VALUES': OpCode.VALUES, 'PICKITEM': OpCode.PICKITEM, 'APPEND': OpCode.APPEND, 'REVERSEITEMS': OpCode.REVERSEITEMS, 'REMOVE': OpCode.REMOVE, 'CLEARITEMS': OpCode.CLEARITEMS, 'ISNULL': OpCode.ISNULL, 'ISTYPE': OpCode.ISTYPE, 'SYSCALL': OpCode.SYSCALL}
    pass
class PointerStackItem(StackItem):
    def __eq__(self, arg0: StackItem) -> bool: ...
    def __init__(self, script: Script, position: int) -> None: ...
    @property
    def position(self) -> int:
        """
        :type: int
        """
    @property
    def script(self) -> Script:
        """
        :type: Script
        """
    pass
class BooleanStackItem(PrimitiveType, StackItem):
    def __bool_(self) -> bool: ...
    @typing.overload
    def __eq__(self, arg0: StackItem) -> bool: ...
    @typing.overload
    def __eq__(self, arg0: bool) -> bool: ...
    def __init__(self, arg0: bool) -> None: ...
    def __len__(self) -> int: ...
    def __str__(self) -> str: ...
    pass
class ReferenceCounter():
    def __init__(self) -> None: ...
    def add_stack_reference(self, stack_item: StackItem) -> None: ...
    @property
    def count(self) -> int:
        """
        :type: int
        """
    pass
class Script():
    @typing.overload
    def __eq__(self, arg0: Script) -> bool: ...
    @typing.overload
    def __eq__(self, arg0: object) -> bool: ...
    def __ge__(self, arg0: Script) -> bool: ...
    def __gt__(self, arg0: Script) -> bool: ...
    @typing.overload
    def __init__(self) -> None: 
        """
        Create a script from a byte array
        """
    @typing.overload
    def __init__(self, data: bytes) -> None: ...
    def __le__(self, arg0: Script) -> bool: ...
    def __len__(self) -> int: ...
    def __lt__(self, arg0: Script) -> bool: ...
    def get_instruction(self, arg0: int) -> Instruction: ...
    @property
    def _value(self) -> bytes:
        """
        :type: bytes
        """
    pass
class ScriptBuilder():
    def __init__(self) -> None: ...
    @typing.overload
    def emit(self, opcode: OpCode) -> ScriptBuilder: ...
    @typing.overload
    def emit(self, opcode: OpCode, data: buffer) -> ScriptBuilder: ...
    def emit_call(self, offset: int) -> ScriptBuilder: ...
    def emit_jump(self, opcode: OpCode, offset: int) -> ScriptBuilder: ...
    @typing.overload
    def emit_push(self, data: bytes) -> ScriptBuilder: ...
    @typing.overload
    def emit_push(self, data: str) -> ScriptBuilder: ...
    @typing.overload
    def emit_push(self, number: BigInteger) -> ScriptBuilder: ...
    @typing.overload
    def emit_push(self, number: int) -> ScriptBuilder: ...
    @typing.overload
    def emit_push(self, with_data: bool) -> ScriptBuilder: ...
    def emit_raw(self, arg0: bytes) -> ScriptBuilder: 
        """
        Push data without applying variable size encoding
        """
    def emit_syscall(self, api_hash: int) -> ScriptBuilder: ...
    def to_array(self) -> bytes: ...
    pass
class Slot():
    def __getitem__(self, arg0: int) -> StackItem: ...
    @typing.overload
    def __init__(self, items: typing.List[StackItem], reference_counter: ReferenceCounter) -> None: ...
    @typing.overload
    def __init__(self, slot_size: int, reference_counter: ReferenceCounter) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __setitem__(self, arg0: int, arg1: StackItem) -> None: ...
    @property
    def items(self) -> list:
        """
        :type: list
        """
    pass
class ArrayStackItem(CompoundType, StackItem):
    def __eq__(self, arg0: StackItem) -> bool: ...
    def __getitem__(self, arg0: int) -> StackItem: ...
    def __init__(self, reference_counter: ReferenceCounter) -> None: 
        """
        Warning: make sure that the reference counter passed in outlives this object.
        Note: This means that creating the reference counter inside the constructor can cause it to be cleaned up by Python before this object's life ended
        """
    def __iter__(self) -> typing.Iterator: 
        """
        Array items.
        """
    def __len__(self) -> int: ...
    def __reversed__(self) -> typing.Iterator: 
        """
        Array items in reversed order.
        """
    def __setitem__(self, arg0: int, arg1: StackItem) -> None: ...
    @typing.overload
    def append(self, stack_item: StackItem) -> None: ...
    @typing.overload
    def append(self, stack_items: typing.List[StackItem]) -> None: ...
    def clear(self) -> None: 
        """
        Remove all internal items.
        """
    def remove(self, index: int) -> None: 
        """
        Remove element by index
        """
    @property
    def _items(self) -> typing.List[StackItem]:
        """
        :type: typing.List[StackItem]
        """
    @property
    def _sub_items(self) -> typing.List[StackItem]:
        """
        :type: typing.List[StackItem]
        """
    pass
class StackItemType():
    """
    Members:

      ANY

      POINTER

      BOOLEAN

      INTEGER

      BYTESTRING

      BUFFER

      ARRAY

      STRUCT

      MAP

      INTEROP
    """
    def __index__(self) -> int: ...
    def __init__(self, arg0: int) -> None: ...
    def __int_(self) -> int: ...
    @property
    def name(self) -> str:
        """
        (self: handle) -> str

        :type: str
        """
    ANY: neo3vm.StackItemType # value = StackItemType.ANY
    ARRAY: neo3vm.StackItemType # value = StackItemType.ARRAY
    BOOLEAN: neo3vm.StackItemType # value = StackItemType.BOOLEAN
    BUFFER: neo3vm.StackItemType # value = StackItemType.BUFFER
    BYTESTRING: neo3vm.StackItemType # value = StackItemType.BYTESTRING
    INTEGER: neo3vm.StackItemType # value = StackItemType.INTEGER
    INTEROP: neo3vm.StackItemType # value = StackItemType.INTEROP
    MAP: neo3vm.StackItemType # value = StackItemType.MAP
    POINTER: neo3vm.StackItemType # value = StackItemType.POINTER
    STRUCT: neo3vm.StackItemType # value = StackItemType.STRUCT
    __members__: dict # value = {'ANY': StackItemType.ANY, 'POINTER': StackItemType.POINTER, 'BOOLEAN': StackItemType.BOOLEAN, 'INTEGER': StackItemType.INTEGER, 'BYTESTRING': StackItemType.BYTESTRING, 'BUFFER': StackItemType.BUFFER, 'ARRAY': StackItemType.ARRAY, 'STRUCT': StackItemType.STRUCT, 'MAP': StackItemType.MAP, 'INTEROP': StackItemType.INTEROP}
    pass
class StructStackItem(ArrayStackItem, CompoundType, StackItem):
    def __init__(self, reference_counter: ReferenceCounter) -> None: 
        """
        Warning: make sure that the reference counter passed in outlives this object.
        Note: This means that creating the reference counter inside the constructor can cause it to be cleaned up by Python before this object's life ended
        """
    pass
class VMState():
    """
    Members:

      NONE

      HALT

      FAULT

      BREAK
    """
    def __index__(self) -> int: ...
    def __init__(self, arg0: int) -> None: ...
    def __int_(self) -> int: ...
    @property
    def name(self) -> str:
        """
        (self: handle) -> str

        :type: str
        """
    BREAK: neo3vm.VMState # value = VMState.BREAK
    FAULT: neo3vm.VMState # value = VMState.FAULT
    HALT: neo3vm.VMState # value = VMState.HALT
    NONE: neo3vm.VMState # value = VMState.NONE
    __members__: dict # value = {'NONE': VMState.NONE, 'HALT': VMState.HALT, 'FAULT': VMState.FAULT, 'BREAK': VMState.BREAK}
    pass
