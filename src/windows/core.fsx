module Core =
    let pause () =
    #if !DEBUG
        printfn "Press any key to continue..."
        System.Console.ReadKey true |> ignore
    #endif
        ()
