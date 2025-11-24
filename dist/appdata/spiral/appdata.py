kernels_aux = r"""
// The types of these two will be replaced during compilation by the Spiral code generator. 
// It matches on `using default_int = ` and `;` with the inner part being replaced so the form should be kept as is. 
// The two statements need to begin at the start of a line.
using default_int = int;
using default_uint = unsigned int;

#ifndef __NVRTC__
// NVRTC has these includes by default so they need to be left out if it is used as the compiler.
#include <new>
#include <assert.h>
#include <stdio.h>
#endif

// For error checking on the host.
#define gpuErrchk(ans) { gpuAssert((ans), __FILE__, __LINE__); }
template <typename T> inline __device__ void destroy(T& obj) { obj.~T(); }
inline void gpuAssert(cudaError error, const char *file, int line, bool abort=true) {
    if (error != cudaSuccess) {
        fprintf(stderr, "GPUassert: %s %s %d\n", cudaGetErrorString(error), file, line);
        if (abort) exit(error);
    }
}

template <typename el>
struct sptr // Shared pointer for the Spiral datatypes. They have to have the refc field inside them to work.
{
    el* base;

    __device__ sptr() : base(nullptr) {}
    __device__ sptr(el* ptr) : base(ptr) { this->base->refc++; }

    __device__ ~sptr()
    {
        if (this->base != nullptr && --this->base->refc == 0)
        {
            delete this->base;
            this->base = nullptr;
        }
    }

    __device__ sptr(sptr& x)
    {
        this->base = x.base;
        this->base->refc++;
    }

    __device__ sptr(sptr&& x)
    {
        this->base = x.base;
        x.base = nullptr;
    }

    __device__ sptr& operator=(sptr& x)
    {
        if (this->base != x.base)
        {
            delete this->base;
            this->base = x.base;
            this->base->refc++;
        }
        return *this;
    }

    __device__ sptr& operator=(sptr&& x)
    {
        if (this->base != x.base)
        {
            delete this->base;
            this->base = x.base;
            x.base = nullptr;
        }
        return *this;
    }
};

template <typename el>
struct csptr : public sptr<el>
{ // Shared pointer for closures specifically.
    using sptr<el>::sptr;
    template <typename... Args>
    __device__ auto operator()(Args... args) -> decltype(this->base->operator()(args...))
    {
        return this->base->operator()(args...);
    }
};

template <typename el, default_int max_length>
struct static_array
{
    el ptr[max_length];
    __device__ el& operator[](default_int i) {
        assert("The index has to be in range." && 0 <= i && i < max_length);
        return this->ptr[i];
    }
};

template <typename el, default_int max_length>
struct static_array_list
{
    default_int length{ 0 };
    el ptr[max_length];

    __device__ el& operator[](default_int i) {
        assert("The index has to be in range." && 0 <= i && i < this->length);
        return this->ptr[i];
    }
    __device__ void push(el& x) {
        ptr[this->length++] = x;
        assert("The array after pushing should not be greater than max length." && this->length <= max_length);
    }
    __device__ void push(el&& x) {
        ptr[this->length++] = std::move(x);
        assert("The array after pushing should not be greater than max length." && this->length <= max_length);
    }
    __device__ el pop() {
        assert("The array before popping should be greater than 0." && 0 < this->length);
        auto x = ptr[--this->length];
        ptr[this->length].~el();
        new (&ptr[this->length]) el();
        return x;
    }
    // Should be used only during initialization.
    __device__ void unsafe_set_length(default_int i) {
        assert("The new length should be in range." && 0 <= i && i <= max_length);
        this->length = i;
    }
};

template <typename el, default_int max_length>
struct dynamic_array_base
{
    int refc{ 0 };
    el* ptr;

    __device__ dynamic_array_base() : ptr(new el[max_length]) {}
    __device__ ~dynamic_array_base() { delete[] this->ptr; }

    __device__ el& operator[](default_int i) {
        assert("The index has to be in range." && 0 <= i && i < this->length);
        return this->ptr[i];
    }
};

template <typename el, default_int max_length>
struct dynamic_array
{
    sptr<dynamic_array_base<el, max_length>> ptr;

    __device__ dynamic_array() = default;
    __device__ dynamic_array(bool t) : ptr(new dynamic_array_base<el, max_length>()) {}
    __device__ el& operator[](default_int i) {
        return this->ptr.base->operator[](i);
    }
};

template <typename el, default_int max_length>
struct dynamic_array_list_base
{
    int refc{ 0 };
    default_int length{ 0 };
    el* ptr;

    __device__ dynamic_array_list_base() : ptr(new el[max_length]) {}
    __device__ dynamic_array_list_base(default_int l) : ptr(new el[max_length]) { this->unsafe_set_length(l); }
    __device__ ~dynamic_array_list_base() { delete[] this->ptr; }

    __device__ el& operator[](default_int i) {
        assert("The index has to be in range." && 0 <= i && i < this->length);
        return this->ptr[i];
    }
    __device__ void push(el& x) {
        ptr[this->length++] = x;
        assert("The array after pushing should not be greater than max length." && this->length <= max_length);
    }
    __device__ void push(el&& x) {
        ptr[this->length++] = std::move(x);
        assert("The array after pushing should not be greater than max length." && this->length <= max_length);
    }
    __device__ el pop() {
        assert("The array before popping should be greater than 0." && 0 < this->length);
        auto x = ptr[--this->length];
        ptr[this->length].~el();
        new (&ptr[this->length]) el();
        return x;
    }
    // Should be used only during initialization.
    __device__ void unsafe_set_length(default_int i) {
        assert("The new length should be in range." && 0 <= i && i <= max_length);
        this->length = i;
    }
};

template <typename el, default_int max_length>
struct dynamic_array_list
{
    sptr<dynamic_array_list_base<el, max_length>> ptr;

    __device__ dynamic_array_list() = default;
    __device__ dynamic_array_list(default_int l) : ptr(new dynamic_array_list_base<el, max_length>(l)) {}

    __device__ el& operator[](default_int i) {
        return this->ptr.base->operator[](i);
    }
    __device__ void push(el& x) {
        this->ptr.base->push(x);
    }
    __device__ void push(el&& x) {
        this->ptr.base->push(std::move(x));
    }
    __device__ el pop() {
        return this->ptr.base->pop();
    }
    // Should be used only during initialization.
    __device__ void unsafe_set_length(default_int i) {
        this->ptr.base->unsafe_set_length(i);
    }
    __device__ default_int length_() {
        return this->ptr.base->length;
    }
};
"""
class static_array():
    def __init__(self, length):
        self.ptr = []
        for _ in range(length):
            self.ptr.append(None)

    def __getitem__(self, index):
        assert 0 <= index < len(self.ptr), "The get index needs to be in range."
        return self.ptr[index]
    
    def __setitem__(self, index, value):
        assert 0 <= index < len(self.ptr), "The set index needs to be in range."
        self.ptr[index] = value

class static_array_list(static_array):
    def __init__(self, length):
        super().__init__(length)
        self.length = 0

    def __getitem__(self, index):
        assert 0 <= index < self.length, "The get index needs to be in range."
        return self.ptr[index]
    
    def __setitem__(self, index, value):
        assert 0 <= index < self.length, "The set index needs to be in range."
        self.ptr[index] = value

    def push(self,value):
        assert (self.length < len(self.ptr)), "The length before pushing has to be less than the maximum length of the array."
        self.ptr[self.length] = value
        self.length += 1

    def pop(self):
        assert (0 < self.length), "The length before popping has to be greater than 0."
        self.length -= 1
        return self.ptr[self.length]

    def unsafe_set_length(self,i):
        assert 0 <= i <= len(self.ptr), "The new length has to be in range."
        self.length = i

class dynamic_array(static_array): 
    pass

class dynamic_array_list(static_array_list):
    def length_(self): return self.length


kernels_main = r"""
"""
from appdata_auto import *
kernels = kernels_aux + kernels_main
import cupy as cp
import numpy as np
from dataclasses import dataclass
from typing import NamedTuple, Union, Callable, Tuple
i8 = int; i16 = int; i32 = int; i64 = int; u8 = int; u16 = int; u32 = int; u64 = int; f32 = float; f64 = float; char = str; string = str
cuda = False


# fwd_dcls
# types
class US2_0(NamedTuple): # (0, Wasm)
    tag = 0
class US2_1(NamedTuple): # (1, Contract)
    tag = 1
US2 = Union[US2_0, US2_1]
class US1_0(NamedTuple): # (0, Some)
    v0 : US2
    tag = 0
class US1_1(NamedTuple): # (1, None)
    tag = 1
US1 = Union[US1_0, US1_1]
class US0_0(NamedTuple): # (0, Gleam)
    tag = 0
class US0_1(NamedTuple): # (1, Lua)
    tag = 1
class US0_2(NamedTuple): # (2, Fsharp)
    tag = 2
class US0_3(NamedTuple): # (3, Cuda)
    tag = 3
class US0_4(NamedTuple): # (4, Cpp)
    tag = 4
class US0_5(NamedTuple): # (5, Rust)
    v0 : US1
    tag = 5
class US0_6(NamedTuple): # (6, TypeScript)
    tag = 6
class US0_7(NamedTuple): # (7, Python)
    tag = 7
US0 = Union[US0_0, US0_1, US0_2, US0_3, US0_4, US0_5, US0_6, US0_7]
@dataclass
class Mut0:
    v0 : string
class US3_0(NamedTuple): # (0, Some)
    v0 : string
    tag = 0
class US3_1(NamedTuple): # (1, None)
    tag = 1
US3 = Union[US3_0, US3_1]
# functions
def method1(v0 : Mut0, v1 : string) -> None:
    v2 = v0.v0
    v6 = v2 + v1 
    del v1, v2
    v0.v0 = v6
    del v0, v6
    return 
def method0(v0 : US0) -> string:
    v12 = ""
    v13 = Mut0(v12)
    del v12
    v17 = f"{v0}"
    del v0
    method1(v13, v17)
    del v17
    v149 = v13.v0
    del v13
    return v149
def method3(v0 : Mut0) -> None:
    v1 = v0.v0
    v8 = "{ "
    v9 = v1 + v8 
    del v1, v8
    v0.v0 = v9
    del v0, v9
    return 
def method4(v0 : Mut0) -> None:
    v1 = v0.v0
    v8 = "tests"
    v9 = v1 + v8 
    del v1, v8
    v0.v0 = v9
    del v0, v9
    return 
def method5(v0 : Mut0) -> None:
    v1 = v0.v0
    v8 = " = "
    v9 = v1 + v8 
    del v1, v8
    v0.v0 = v9
    del v0, v9
    return 
def method6(v0 : Mut0) -> None:
    v1 = v0.v0
    v8 = "; "
    v9 = v1 + v8 
    del v1, v8
    v0.v0 = v9
    del v0, v9
    return 
def method7(v0 : Mut0) -> None:
    v1 = v0.v0
    v8 = "backends"
    v9 = v1 + v8 
    del v1, v8
    v0.v0 = v9
    del v0, v9
    return 
def method8(v0 : Mut0) -> None:
    v1 = v0.v0
    v8 = " }"
    v9 = v1 + v8 
    del v1, v8
    v0.v0 = v9
    del v0, v9
    return 
def method2(v0 : bool, v1 : (cp if cuda else np).ndarray) -> string:
    v13 = ""
    v14 = Mut0(v13)
    del v13
    method3(v14)
    method4(v14)
    method5(v14)
    if v0:
        v390 = "true"
        v392 = v390
    else:
        v391 = "false"
        v392 = v391
    del v0
    method1(v14, v392)
    del v392
    method6(v14)
    method7(v14)
    method5(v14)
    v925 = f"{v1}"
    del v1
    method1(v14, v925)
    del v925
    method8(v14)
    v1182 = v14.v0
    del v14
    return v1182
# main_defs
def main_body():
    
    
    
    
    
    v3 = None
    
    
    v36 = US0_0()
    v37 = method0(v36)
    del v36
    v81 = "("
    v82 = v37.split(v81)
    del v37
    v96 = v82[0]
    del v82
    v107 = US0_7()
    v108 = method0(v107)
    del v107
    v112 = v108.startswith(v96)
    del v96, v108
    if v112:
        v123 = "Gleam"
        v126 = US3_0(v123)
    else:
        v126 = US3_1()
    del v112
    match v126:
        case US3_1(): # None
            v151 = US0_1()
            v152 = method0(v151)
            del v151
            v194 = v152.split(v81)
            del v152
            v208 = v194[0]
            del v194
            v219 = US0_7()
            v220 = method0(v219)
            del v219
            v224 = v220.startswith(v208)
            del v208, v220
            if v224:
                v235 = "Lua"
                v238 = US3_0(v235)
            else:
                v238 = US3_1()
            del v224
            match v238:
                case US3_1(): # None
                    del v238
                    v263 = US0_2()
                    v264 = method0(v263)
                    del v263
                    v306 = v264.split(v81)
                    del v264
                    v320 = v306[0]
                    del v306
                    v331 = US0_7()
                    v332 = method0(v331)
                    del v331
                    v336 = v332.startswith(v320)
                    del v320, v332
                    if v336:
                        v347 = "Fsharp"
                        v350 = US3_0(v347)
                    else:
                        v350 = US3_1()
                    del v336
                    match v350:
                        case US3_1(): # None
                            del v350
                            v375 = US0_3()
                            v376 = method0(v375)
                            del v375
                            v418 = v376.split(v81)
                            del v376
                            v432 = v418[0]
                            del v418
                            v443 = US0_7()
                            v444 = method0(v443)
                            del v443
                            v448 = v444.startswith(v432)
                            del v432, v444
                            if v448:
                                v459 = "Cuda"
                                v462 = US3_0(v459)
                            else:
                                v462 = US3_1()
                            del v448
                            match v462:
                                case US3_1(): # None
                                    del v462
                                    v487 = US0_4()
                                    v488 = method0(v487)
                                    del v487
                                    v530 = v488.split(v81)
                                    del v488
                                    v544 = v530[0]
                                    del v530
                                    v555 = US0_7()
                                    v556 = method0(v555)
                                    del v555
                                    v560 = v556.startswith(v544)
                                    del v544, v556
                                    if v560:
                                        v571 = "Cpp"
                                        v574 = US3_0(v571)
                                    else:
                                        v574 = US3_1()
                                    del v560
                                    match v574:
                                        case US3_1(): # None
                                            del v574
                                            v599 = US0_5(v3)
                                            v600 = method0(v599)
                                            del v599
                                            v642 = v600.split(v81)
                                            del v600
                                            v656 = v642[0]
                                            del v642
                                            v667 = US0_7()
                                            v668 = method0(v667)
                                            del v667
                                            v672 = v668.startswith(v656)
                                            del v656, v668
                                            if v672:
                                                v683 = "Rust"
                                                v686 = US3_0(v683)
                                            else:
                                                v686 = US3_1()
                                            del v672
                                            match v686:
                                                case US3_1(): # None
                                                    del v686
                                                    v711 = US0_6()
                                                    v712 = method0(v711)
                                                    del v711
                                                    v754 = v712.split(v81)
                                                    del v712
                                                    v768 = v754[0]
                                                    del v754
                                                    v779 = US0_7()
                                                    v780 = method0(v779)
                                                    del v779
                                                    v784 = v780.startswith(v768)
                                                    del v768, v780
                                                    if v784:
                                                        v795 = "TypeScript"
                                                        v798 = US3_0(v795)
                                                    else:
                                                        v798 = US3_1()
                                                    del v784
                                                    match v798:
                                                        case US3_1(): # None
                                                            del v798
                                                            v801 = "Python"
                                                            v816 = US3_0(v801)
                                                        case US3_0(v799): # Some
                                                            del v798
                                                            v816 = US3_0(v799)
                                                        case t:
                                                            raise Exception(f'Pattern matching miss. Got: {t}')
                                                case US3_0(v687): # Some
                                                    del v686
                                                    v816 = US3_0(v687)
                                                case t:
                                                    raise Exception(f'Pattern matching miss. Got: {t}')
                                        case US3_0(v575): # Some
                                            del v574
                                            v816 = US3_0(v575)
                                        case t:
                                            raise Exception(f'Pattern matching miss. Got: {t}')
                                case US3_0(v463): # Some
                                    del v462
                                    v816 = US3_0(v463)
                                case t:
                                    raise Exception(f'Pattern matching miss. Got: {t}')
                        case US3_0(v351): # Some
                            del v350
                            v816 = US3_0(v351)
                        case t:
                            raise Exception(f'Pattern matching miss. Got: {t}')
                case US3_0(v239): # Some
                    del v238
                    v816 = US3_0(v239)
                case t:
                    raise Exception(f'Pattern matching miss. Got: {t}')
        case US3_0(v127): # Some
            v816 = US3_0(v127)
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v3, v126
    match v816:
        case US3_1(): # None
            raise Exception("Option does not have a value.")
        case US3_0(v817): # Some
            v820 = v817
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v816
    
    
    
    
    
    v824 = None
    
    
    v857 = US0_0()
    v858 = method0(v857)
    del v857
    v900 = v858.split(v81)
    del v858
    v914 = v900[0]
    del v900
    v925 = US0_6()
    v926 = method0(v925)
    del v925
    v930 = v926.startswith(v914)
    del v914, v926
    if v930:
        v941 = "Gleam"
        v944 = US3_0(v941)
    else:
        v944 = US3_1()
    del v930
    match v944:
        case US3_1(): # None
            v969 = US0_1()
            v970 = method0(v969)
            del v969
            v1012 = v970.split(v81)
            del v970
            v1026 = v1012[0]
            del v1012
            v1037 = US0_6()
            v1038 = method0(v1037)
            del v1037
            v1042 = v1038.startswith(v1026)
            del v1026, v1038
            if v1042:
                v1053 = "Lua"
                v1056 = US3_0(v1053)
            else:
                v1056 = US3_1()
            del v1042
            match v1056:
                case US3_1(): # None
                    del v1056
                    v1081 = US0_2()
                    v1082 = method0(v1081)
                    del v1081
                    v1124 = v1082.split(v81)
                    del v1082
                    v1138 = v1124[0]
                    del v1124
                    v1149 = US0_6()
                    v1150 = method0(v1149)
                    del v1149
                    v1154 = v1150.startswith(v1138)
                    del v1138, v1150
                    if v1154:
                        v1165 = "Fsharp"
                        v1168 = US3_0(v1165)
                    else:
                        v1168 = US3_1()
                    del v1154
                    match v1168:
                        case US3_1(): # None
                            del v1168
                            v1193 = US0_3()
                            v1194 = method0(v1193)
                            del v1193
                            v1236 = v1194.split(v81)
                            del v1194
                            v1250 = v1236[0]
                            del v1236
                            v1261 = US0_6()
                            v1262 = method0(v1261)
                            del v1261
                            v1266 = v1262.startswith(v1250)
                            del v1250, v1262
                            if v1266:
                                v1277 = "Cuda"
                                v1280 = US3_0(v1277)
                            else:
                                v1280 = US3_1()
                            del v1266
                            match v1280:
                                case US3_1(): # None
                                    del v1280
                                    v1305 = US0_4()
                                    v1306 = method0(v1305)
                                    del v1305
                                    v1348 = v1306.split(v81)
                                    del v1306
                                    v1362 = v1348[0]
                                    del v1348
                                    v1373 = US0_6()
                                    v1374 = method0(v1373)
                                    del v1373
                                    v1378 = v1374.startswith(v1362)
                                    del v1362, v1374
                                    if v1378:
                                        v1389 = "Cpp"
                                        v1392 = US3_0(v1389)
                                    else:
                                        v1392 = US3_1()
                                    del v1378
                                    match v1392:
                                        case US3_1(): # None
                                            del v1392
                                            v1417 = US0_5(v824)
                                            v1418 = method0(v1417)
                                            del v1417
                                            v1460 = v1418.split(v81)
                                            del v1418
                                            v1474 = v1460[0]
                                            del v1460
                                            v1485 = US0_6()
                                            v1486 = method0(v1485)
                                            del v1485
                                            v1490 = v1486.startswith(v1474)
                                            del v1474, v1486
                                            if v1490:
                                                v1501 = "Rust"
                                                v1504 = US3_0(v1501)
                                            else:
                                                v1504 = US3_1()
                                            del v1490
                                            match v1504:
                                                case US3_1(): # None
                                                    del v1504
                                                    v1507 = "TypeScript"
                                                    v1520 = US3_0(v1507)
                                                case US3_0(v1505): # Some
                                                    del v1504
                                                    v1520 = US3_0(v1505)
                                                case t:
                                                    raise Exception(f'Pattern matching miss. Got: {t}')
                                        case US3_0(v1393): # Some
                                            del v1392
                                            v1520 = US3_0(v1393)
                                        case t:
                                            raise Exception(f'Pattern matching miss. Got: {t}')
                                case US3_0(v1281): # Some
                                    del v1280
                                    v1520 = US3_0(v1281)
                                case t:
                                    raise Exception(f'Pattern matching miss. Got: {t}')
                        case US3_0(v1169): # Some
                            del v1168
                            v1520 = US3_0(v1169)
                        case t:
                            raise Exception(f'Pattern matching miss. Got: {t}')
                case US3_0(v1057): # Some
                    del v1056
                    v1520 = US3_0(v1057)
                case t:
                    raise Exception(f'Pattern matching miss. Got: {t}')
        case US3_0(v945): # Some
            v1520 = US3_0(v945)
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v824, v944
    match v1520:
        case US3_1(): # None
            raise Exception("Option does not have a value.")
        case US3_0(v1521): # Some
            v1524 = v1521
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v1520
    
    
    
    
    
    v1528 = None
    
    
    v1561 = US0_0()
    v1562 = method0(v1561)
    del v1561
    v1604 = v1562.split(v81)
    del v1562
    v1618 = v1604[0]
    del v1604
    v1629 = US2_1()
    v1630 = US1_0(v1629)
    del v1629
    v1631 = US0_5(v1630)
    del v1630
    v1632 = method0(v1631)
    del v1631
    v1636 = v1632.startswith(v1618)
    del v1618, v1632
    if v1636:
        v1647 = "Gleam"
        v1650 = US3_0(v1647)
    else:
        v1650 = US3_1()
    del v1636
    match v1650:
        case US3_1(): # None
            v1675 = US0_1()
            v1676 = method0(v1675)
            del v1675
            v1718 = v1676.split(v81)
            del v1676
            v1732 = v1718[0]
            del v1718
            v1743 = US2_1()
            v1744 = US1_0(v1743)
            del v1743
            v1745 = US0_5(v1744)
            del v1744
            v1746 = method0(v1745)
            del v1745
            v1750 = v1746.startswith(v1732)
            del v1732, v1746
            if v1750:
                v1761 = "Lua"
                v1764 = US3_0(v1761)
            else:
                v1764 = US3_1()
            del v1750
            match v1764:
                case US3_1(): # None
                    del v1764
                    v1789 = US0_2()
                    v1790 = method0(v1789)
                    del v1789
                    v1832 = v1790.split(v81)
                    del v1790
                    v1846 = v1832[0]
                    del v1832
                    v1857 = US2_1()
                    v1858 = US1_0(v1857)
                    del v1857
                    v1859 = US0_5(v1858)
                    del v1858
                    v1860 = method0(v1859)
                    del v1859
                    v1864 = v1860.startswith(v1846)
                    del v1846, v1860
                    if v1864:
                        v1875 = "Fsharp"
                        v1878 = US3_0(v1875)
                    else:
                        v1878 = US3_1()
                    del v1864
                    match v1878:
                        case US3_1(): # None
                            del v1878
                            v1903 = US0_3()
                            v1904 = method0(v1903)
                            del v1903
                            v1946 = v1904.split(v81)
                            del v1904
                            v1960 = v1946[0]
                            del v1946
                            v1971 = US2_1()
                            v1972 = US1_0(v1971)
                            del v1971
                            v1973 = US0_5(v1972)
                            del v1972
                            v1974 = method0(v1973)
                            del v1973
                            v1978 = v1974.startswith(v1960)
                            del v1960, v1974
                            if v1978:
                                v1989 = "Cuda"
                                v1992 = US3_0(v1989)
                            else:
                                v1992 = US3_1()
                            del v1978
                            match v1992:
                                case US3_1(): # None
                                    del v1992
                                    v2017 = US0_4()
                                    v2018 = method0(v2017)
                                    del v2017
                                    v2060 = v2018.split(v81)
                                    del v2018
                                    v2074 = v2060[0]
                                    del v2060
                                    v2085 = US2_1()
                                    v2086 = US1_0(v2085)
                                    del v2085
                                    v2087 = US0_5(v2086)
                                    del v2086
                                    v2088 = method0(v2087)
                                    del v2087
                                    v2092 = v2088.startswith(v2074)
                                    del v2074, v2088
                                    if v2092:
                                        v2103 = "Cpp"
                                        v2106 = US3_0(v2103)
                                    else:
                                        v2106 = US3_1()
                                    del v2092
                                    match v2106:
                                        case US3_1(): # None
                                            del v2106
                                            match v1528:
                                                case US1_0(v2109): # Some
                                                    match v2109:
                                                        case US2_1(): # Contract
                                                            del v2109
                                                            v2111 = True
                                                        case t:
                                                            del v2109
                                                            v2111 = False
                                                case t:
                                                    v2111 = False
                                            if v2111:
                                                v2112 = "Rust"
                                                v2226 = US3_0(v2112)
                                            else:
                                                v2136 = US0_5(v1528)
                                                v2137 = method0(v2136)
                                                del v2136
                                                v2179 = v2137.split(v81)
                                                del v2137
                                                v2193 = v2179[0]
                                                del v2179
                                                v2204 = US2_1()
                                                v2205 = US1_0(v2204)
                                                del v2204
                                                v2206 = US0_5(v2205)
                                                del v2205
                                                v2207 = method0(v2206)
                                                del v2206
                                                v2211 = v2207.startswith(v2193)
                                                del v2193, v2207
                                                if v2211:
                                                    del v2211
                                                    v2222 = "Rust"
                                                    v2226 = US3_0(v2222)
                                                else:
                                                    del v2211
                                                    v2226 = US3_1()
                                            del v2111
                                            match v2226:
                                                case US3_1(): # None
                                                    del v2226
                                                    v2251 = US0_6()
                                                    v2252 = method0(v2251)
                                                    del v2251
                                                    v2294 = v2252.split(v81)
                                                    del v2252
                                                    v2308 = v2294[0]
                                                    del v2294
                                                    v2319 = US2_1()
                                                    v2320 = US1_0(v2319)
                                                    del v2319
                                                    v2321 = US0_5(v2320)
                                                    del v2320
                                                    v2322 = method0(v2321)
                                                    del v2321
                                                    v2326 = v2322.startswith(v2308)
                                                    del v2308, v2322
                                                    if v2326:
                                                        v2337 = "TypeScript"
                                                        v2340 = US3_0(v2337)
                                                    else:
                                                        v2340 = US3_1()
                                                    del v2326
                                                    match v2340:
                                                        case US3_1(): # None
                                                            del v2340
                                                            v2365 = US0_7()
                                                            v2366 = method0(v2365)
                                                            del v2365
                                                            v2408 = v2366.split(v81)
                                                            del v2366
                                                            v2422 = v2408[0]
                                                            del v2408
                                                            v2433 = US2_1()
                                                            v2434 = US1_0(v2433)
                                                            del v2433
                                                            v2435 = US0_5(v2434)
                                                            del v2434
                                                            v2436 = method0(v2435)
                                                            del v2435
                                                            v2440 = v2436.startswith(v2422)
                                                            del v2422, v2436
                                                            if v2440:
                                                                v2451 = "Python"
                                                                v2454 = US3_0(v2451)
                                                            else:
                                                                v2454 = US3_1()
                                                            del v2440
                                                            match v2454:
                                                                case US3_1(): # None
                                                                    del v2454
                                                                    v2473 = US3_1()
                                                                case US3_0(v2455): # Some
                                                                    del v2454
                                                                    v2473 = US3_0(v2455)
                                                                case t:
                                                                    raise Exception(f'Pattern matching miss. Got: {t}')
                                                        case US3_0(v2341): # Some
                                                            del v2340
                                                            v2473 = US3_0(v2341)
                                                        case t:
                                                            raise Exception(f'Pattern matching miss. Got: {t}')
                                                case US3_0(v2227): # Some
                                                    del v2226
                                                    v2473 = US3_0(v2227)
                                                case t:
                                                    raise Exception(f'Pattern matching miss. Got: {t}')
                                        case US3_0(v2107): # Some
                                            del v2106
                                            v2473 = US3_0(v2107)
                                        case t:
                                            raise Exception(f'Pattern matching miss. Got: {t}')
                                case US3_0(v1993): # Some
                                    del v1992
                                    v2473 = US3_0(v1993)
                                case t:
                                    raise Exception(f'Pattern matching miss. Got: {t}')
                        case US3_0(v1879): # Some
                            del v1878
                            v2473 = US3_0(v1879)
                        case t:
                            raise Exception(f'Pattern matching miss. Got: {t}')
                case US3_0(v1765): # Some
                    del v1764
                    v2473 = US3_0(v1765)
                case t:
                    raise Exception(f'Pattern matching miss. Got: {t}')
        case US3_0(v1651): # Some
            v2473 = US3_0(v1651)
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v1528, v1650
    match v2473:
        case US3_1(): # None
            raise Exception("Option does not have a value.")
        case US3_0(v2474): # Some
            v2477 = v2474
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v2473
    
    
    
    
    
    v2481 = None
    
    
    v2514 = US0_0()
    v2515 = method0(v2514)
    del v2514
    v2557 = v2515.split(v81)
    del v2515
    v2571 = v2557[0]
    del v2557
    v2582 = US2_0()
    v2583 = US1_0(v2582)
    del v2582
    v2584 = US0_5(v2583)
    del v2583
    v2585 = method0(v2584)
    del v2584
    v2589 = v2585.startswith(v2571)
    del v2571, v2585
    if v2589:
        v2600 = "Gleam"
        v2603 = US3_0(v2600)
    else:
        v2603 = US3_1()
    del v2589
    match v2603:
        case US3_1(): # None
            v2628 = US0_1()
            v2629 = method0(v2628)
            del v2628
            v2671 = v2629.split(v81)
            del v2629
            v2685 = v2671[0]
            del v2671
            v2696 = US2_0()
            v2697 = US1_0(v2696)
            del v2696
            v2698 = US0_5(v2697)
            del v2697
            v2699 = method0(v2698)
            del v2698
            v2703 = v2699.startswith(v2685)
            del v2685, v2699
            if v2703:
                v2714 = "Lua"
                v2717 = US3_0(v2714)
            else:
                v2717 = US3_1()
            del v2703
            match v2717:
                case US3_1(): # None
                    del v2717
                    v2742 = US0_2()
                    v2743 = method0(v2742)
                    del v2742
                    v2785 = v2743.split(v81)
                    del v2743
                    v2799 = v2785[0]
                    del v2785
                    v2810 = US2_0()
                    v2811 = US1_0(v2810)
                    del v2810
                    v2812 = US0_5(v2811)
                    del v2811
                    v2813 = method0(v2812)
                    del v2812
                    v2817 = v2813.startswith(v2799)
                    del v2799, v2813
                    if v2817:
                        v2828 = "Fsharp"
                        v2831 = US3_0(v2828)
                    else:
                        v2831 = US3_1()
                    del v2817
                    match v2831:
                        case US3_1(): # None
                            del v2831
                            v2856 = US0_3()
                            v2857 = method0(v2856)
                            del v2856
                            v2899 = v2857.split(v81)
                            del v2857
                            v2913 = v2899[0]
                            del v2899
                            v2924 = US2_0()
                            v2925 = US1_0(v2924)
                            del v2924
                            v2926 = US0_5(v2925)
                            del v2925
                            v2927 = method0(v2926)
                            del v2926
                            v2931 = v2927.startswith(v2913)
                            del v2913, v2927
                            if v2931:
                                v2942 = "Cuda"
                                v2945 = US3_0(v2942)
                            else:
                                v2945 = US3_1()
                            del v2931
                            match v2945:
                                case US3_1(): # None
                                    del v2945
                                    v2970 = US0_4()
                                    v2971 = method0(v2970)
                                    del v2970
                                    v3013 = v2971.split(v81)
                                    del v2971
                                    v3027 = v3013[0]
                                    del v3013
                                    v3038 = US2_0()
                                    v3039 = US1_0(v3038)
                                    del v3038
                                    v3040 = US0_5(v3039)
                                    del v3039
                                    v3041 = method0(v3040)
                                    del v3040
                                    v3045 = v3041.startswith(v3027)
                                    del v3027, v3041
                                    if v3045:
                                        v3056 = "Cpp"
                                        v3059 = US3_0(v3056)
                                    else:
                                        v3059 = US3_1()
                                    del v3045
                                    match v3059:
                                        case US3_1(): # None
                                            del v3059
                                            match v2481:
                                                case US1_0(v3062): # Some
                                                    match v3062:
                                                        case US2_0(): # Wasm
                                                            del v3062
                                                            v3064 = True
                                                        case t:
                                                            del v3062
                                                            v3064 = False
                                                case t:
                                                    v3064 = False
                                            if v3064:
                                                v3065 = "Rust"
                                                v3179 = US3_0(v3065)
                                            else:
                                                v3089 = US0_5(v2481)
                                                v3090 = method0(v3089)
                                                del v3089
                                                v3132 = v3090.split(v81)
                                                del v3090
                                                v3146 = v3132[0]
                                                del v3132
                                                v3157 = US2_0()
                                                v3158 = US1_0(v3157)
                                                del v3157
                                                v3159 = US0_5(v3158)
                                                del v3158
                                                v3160 = method0(v3159)
                                                del v3159
                                                v3164 = v3160.startswith(v3146)
                                                del v3146, v3160
                                                if v3164:
                                                    del v3164
                                                    v3175 = "Rust"
                                                    v3179 = US3_0(v3175)
                                                else:
                                                    del v3164
                                                    v3179 = US3_1()
                                            del v3064
                                            match v3179:
                                                case US3_1(): # None
                                                    del v3179
                                                    v3204 = US0_6()
                                                    v3205 = method0(v3204)
                                                    del v3204
                                                    v3247 = v3205.split(v81)
                                                    del v3205
                                                    v3261 = v3247[0]
                                                    del v3247
                                                    v3272 = US2_0()
                                                    v3273 = US1_0(v3272)
                                                    del v3272
                                                    v3274 = US0_5(v3273)
                                                    del v3273
                                                    v3275 = method0(v3274)
                                                    del v3274
                                                    v3279 = v3275.startswith(v3261)
                                                    del v3261, v3275
                                                    if v3279:
                                                        v3290 = "TypeScript"
                                                        v3293 = US3_0(v3290)
                                                    else:
                                                        v3293 = US3_1()
                                                    del v3279
                                                    match v3293:
                                                        case US3_1(): # None
                                                            del v3293
                                                            v3318 = US0_7()
                                                            v3319 = method0(v3318)
                                                            del v3318
                                                            v3361 = v3319.split(v81)
                                                            del v3319
                                                            v3375 = v3361[0]
                                                            del v3361
                                                            v3386 = US2_0()
                                                            v3387 = US1_0(v3386)
                                                            del v3386
                                                            v3388 = US0_5(v3387)
                                                            del v3387
                                                            v3389 = method0(v3388)
                                                            del v3388
                                                            v3393 = v3389.startswith(v3375)
                                                            del v3375, v3389
                                                            if v3393:
                                                                v3404 = "Python"
                                                                v3407 = US3_0(v3404)
                                                            else:
                                                                v3407 = US3_1()
                                                            del v3393
                                                            match v3407:
                                                                case US3_1(): # None
                                                                    del v3407
                                                                    v3426 = US3_1()
                                                                case US3_0(v3408): # Some
                                                                    del v3407
                                                                    v3426 = US3_0(v3408)
                                                                case t:
                                                                    raise Exception(f'Pattern matching miss. Got: {t}')
                                                        case US3_0(v3294): # Some
                                                            del v3293
                                                            v3426 = US3_0(v3294)
                                                        case t:
                                                            raise Exception(f'Pattern matching miss. Got: {t}')
                                                case US3_0(v3180): # Some
                                                    del v3179
                                                    v3426 = US3_0(v3180)
                                                case t:
                                                    raise Exception(f'Pattern matching miss. Got: {t}')
                                        case US3_0(v3060): # Some
                                            del v3059
                                            v3426 = US3_0(v3060)
                                        case t:
                                            raise Exception(f'Pattern matching miss. Got: {t}')
                                case US3_0(v2946): # Some
                                    del v2945
                                    v3426 = US3_0(v2946)
                                case t:
                                    raise Exception(f'Pattern matching miss. Got: {t}')
                        case US3_0(v2832): # Some
                            del v2831
                            v3426 = US3_0(v2832)
                        case t:
                            raise Exception(f'Pattern matching miss. Got: {t}')
                case US3_0(v2718): # Some
                    del v2717
                    v3426 = US3_0(v2718)
                case t:
                    raise Exception(f'Pattern matching miss. Got: {t}')
        case US3_0(v2604): # Some
            v3426 = US3_0(v2604)
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v2481, v2603
    match v3426:
        case US3_1(): # None
            raise Exception("Option does not have a value.")
        case US3_0(v3427): # Some
            v3430 = v3427
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v3426
    
    
    
    
    
    v3434 = None
    del v3434
    
    
    v3467 = US0_0()
    v3468 = method0(v3467)
    del v3467
    v3510 = v3468.split(v81)
    del v3468
    v3524 = v3510[0]
    del v3510
    v3535 = US0_4()
    v3536 = method0(v3535)
    del v3535
    v3540 = v3536.startswith(v3524)
    del v3524, v3536
    if v3540:
        v3551 = "Gleam"
        v3554 = US3_0(v3551)
    else:
        v3554 = US3_1()
    del v3540
    match v3554:
        case US3_1(): # None
            v3579 = US0_1()
            v3580 = method0(v3579)
            del v3579
            v3622 = v3580.split(v81)
            del v3580
            v3636 = v3622[0]
            del v3622
            v3647 = US0_4()
            v3648 = method0(v3647)
            del v3647
            v3652 = v3648.startswith(v3636)
            del v3636, v3648
            if v3652:
                v3663 = "Lua"
                v3666 = US3_0(v3663)
            else:
                v3666 = US3_1()
            del v3652
            match v3666:
                case US3_1(): # None
                    del v3666
                    v3691 = US0_2()
                    v3692 = method0(v3691)
                    del v3691
                    v3734 = v3692.split(v81)
                    del v3692
                    v3748 = v3734[0]
                    del v3734
                    v3759 = US0_4()
                    v3760 = method0(v3759)
                    del v3759
                    v3764 = v3760.startswith(v3748)
                    del v3748, v3760
                    if v3764:
                        v3775 = "Fsharp"
                        v3778 = US3_0(v3775)
                    else:
                        v3778 = US3_1()
                    del v3764
                    match v3778:
                        case US3_1(): # None
                            del v3778
                            v3803 = US0_3()
                            v3804 = method0(v3803)
                            del v3803
                            v3846 = v3804.split(v81)
                            del v3804
                            v3860 = v3846[0]
                            del v3846
                            v3871 = US0_4()
                            v3872 = method0(v3871)
                            del v3871
                            v3876 = v3872.startswith(v3860)
                            del v3860, v3872
                            if v3876:
                                v3887 = "Cuda"
                                v3890 = US3_0(v3887)
                            else:
                                v3890 = US3_1()
                            del v3876
                            match v3890:
                                case US3_1(): # None
                                    del v3890
                                    v3893 = "Cpp"
                                    v3902 = US3_0(v3893)
                                case US3_0(v3891): # Some
                                    del v3890
                                    v3902 = US3_0(v3891)
                                case t:
                                    raise Exception(f'Pattern matching miss. Got: {t}')
                        case US3_0(v3779): # Some
                            del v3778
                            v3902 = US3_0(v3779)
                        case t:
                            raise Exception(f'Pattern matching miss. Got: {t}')
                case US3_0(v3667): # Some
                    del v3666
                    v3902 = US3_0(v3667)
                case t:
                    raise Exception(f'Pattern matching miss. Got: {t}')
        case US3_0(v3555): # Some
            v3902 = US3_0(v3555)
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v3554
    match v3902:
        case US3_1(): # None
            raise Exception("Option does not have a value.")
        case US3_0(v3903): # Some
            v3906 = v3903
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v3902
    
    
    
    
    
    v3910 = None
    del v3910
    
    
    v3943 = US0_0()
    v3944 = method0(v3943)
    del v3943
    v3986 = v3944.split(v81)
    del v3944
    v4000 = v3986[0]
    del v3986
    v4011 = US0_3()
    v4012 = method0(v4011)
    del v4011
    v4016 = v4012.startswith(v4000)
    del v4000, v4012
    if v4016:
        v4027 = "Gleam"
        v4030 = US3_0(v4027)
    else:
        v4030 = US3_1()
    del v4016
    match v4030:
        case US3_1(): # None
            v4055 = US0_1()
            v4056 = method0(v4055)
            del v4055
            v4098 = v4056.split(v81)
            del v4056
            v4112 = v4098[0]
            del v4098
            v4123 = US0_3()
            v4124 = method0(v4123)
            del v4123
            v4128 = v4124.startswith(v4112)
            del v4112, v4124
            if v4128:
                v4139 = "Lua"
                v4142 = US3_0(v4139)
            else:
                v4142 = US3_1()
            del v4128
            match v4142:
                case US3_1(): # None
                    del v4142
                    v4167 = US0_2()
                    v4168 = method0(v4167)
                    del v4167
                    v4210 = v4168.split(v81)
                    del v4168
                    v4224 = v4210[0]
                    del v4210
                    v4235 = US0_3()
                    v4236 = method0(v4235)
                    del v4235
                    v4240 = v4236.startswith(v4224)
                    del v4224, v4236
                    if v4240:
                        v4251 = "Fsharp"
                        v4254 = US3_0(v4251)
                    else:
                        v4254 = US3_1()
                    del v4240
                    match v4254:
                        case US3_1(): # None
                            del v4254
                            v4257 = "Cuda"
                            v4264 = US3_0(v4257)
                        case US3_0(v4255): # Some
                            del v4254
                            v4264 = US3_0(v4255)
                        case t:
                            raise Exception(f'Pattern matching miss. Got: {t}')
                case US3_0(v4143): # Some
                    del v4142
                    v4264 = US3_0(v4143)
                case t:
                    raise Exception(f'Pattern matching miss. Got: {t}')
        case US3_0(v4031): # Some
            v4264 = US3_0(v4031)
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v4030
    match v4264:
        case US3_1(): # None
            raise Exception("Option does not have a value.")
        case US3_0(v4265): # Some
            v4268 = v4265
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v4264
    
    
    
    
    
    v4272 = None
    del v4272
    
    
    v4305 = US0_0()
    v4306 = method0(v4305)
    del v4305
    v4348 = v4306.split(v81)
    del v4306
    v4362 = v4348[0]
    del v4348
    v4373 = US0_2()
    v4374 = method0(v4373)
    del v4373
    v4378 = v4374.startswith(v4362)
    del v4362, v4374
    if v4378:
        v4389 = "Gleam"
        v4392 = US3_0(v4389)
    else:
        v4392 = US3_1()
    del v4378
    match v4392:
        case US3_1(): # None
            v4417 = US0_1()
            v4418 = method0(v4417)
            del v4417
            v4460 = v4418.split(v81)
            del v4418
            v4474 = v4460[0]
            del v4460
            v4485 = US0_2()
            v4486 = method0(v4485)
            del v4485
            v4490 = v4486.startswith(v4474)
            del v4474, v4486
            if v4490:
                v4501 = "Lua"
                v4504 = US3_0(v4501)
            else:
                v4504 = US3_1()
            del v4490
            match v4504:
                case US3_1(): # None
                    del v4504
                    v4507 = "Fsharp"
                    v4512 = US3_0(v4507)
                case US3_0(v4505): # Some
                    del v4504
                    v4512 = US3_0(v4505)
                case t:
                    raise Exception(f'Pattern matching miss. Got: {t}')
        case US3_0(v4393): # Some
            v4512 = US3_0(v4393)
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v4392
    match v4512:
        case US3_1(): # None
            raise Exception("Option does not have a value.")
        case US3_0(v4513): # Some
            v4516 = v4513
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v4512
    
    
    
    
    
    v4520 = None
    del v4520
    
    
    v4553 = US0_0()
    v4554 = method0(v4553)
    del v4553
    v4596 = v4554.split(v81)
    del v81, v4554
    v4610 = v4596[0]
    del v4596
    v4621 = US0_1()
    v4622 = method0(v4621)
    del v4621
    v4626 = v4622.startswith(v4610)
    del v4610, v4622
    if v4626:
        v4637 = "Gleam"
        v4640 = US3_0(v4637)
    else:
        v4640 = US3_1()
    del v4626
    match v4640:
        case US3_1(): # None
            v4643 = "Lua"
            v4646 = US3_0(v4643)
        case US3_0(v4641): # Some
            v4646 = US3_0(v4641)
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v4640
    match v4646:
        case US3_1(): # None
            raise Exception("Option does not have a value.")
        case US3_0(v4647): # Some
            v4650 = v4647
        case t:
            raise Exception(f'Pattern matching miss. Got: {t}')
    del v4646
    
    
    
    
    
    v4654 = None
    del v4654
    
    
    v4665 = []
    v4665.insert(0, v820)
    del v820
    v4669 = v4665 
    del v4665
    v4669.insert(0, v1524)
    del v1524
    v4683 = v4669 
    del v4669
    v4683.insert(0, v2477)
    del v2477
    v4697 = v4683 
    del v4683
    v4697.insert(0, v3430)
    del v3430
    v4711 = v4697 
    del v4697
    v4711.insert(0, v3906)
    del v3906
    v4725 = v4711 
    del v4711
    v4725.insert(0, v4268)
    del v4268
    v4739 = v4725 
    del v4725
    v4739.insert(0, v4516)
    del v4516
    v4753 = v4739 
    del v4739
    v4753.insert(0, v4650)
    del v4650
    v4767 = v4753 
    del v4753
    v4784 = "Gleam"
    v4767.insert(0, v4784)
    del v4784
    v4785 = v4767 
    del v4767
    v4817 = (cp if cuda else np).array(v4785)
    del v4785
    v4828 = True
    v4829 = method2(v4828, v4817)
    del v4817, v4828
    print(v4829)
    del v4829
    return 

def main():
    r = main_body()
    if cuda: cp.cuda.get_current_stream().synchronize() # This line is here so the `__trap()` calls on the kernel aren't missed.
    return r

if __name__ == '__main__': result = main(); None if result is None else print(result)
