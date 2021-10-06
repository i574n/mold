#r "nuget: Argu"
#r "nuget: Fake.Core.Process"

#load "core.fsx"

open System
open Core
open Argu
open Fake.Core
open Fake
open Fake.IO

let path = Path.convertWindowsToCurrentPath "%localappdata%/Microsoft/PowerToys/FancyZones"
printfn $"path={path}"

Core.pause ()
