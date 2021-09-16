namespace Mold

open Farmer
open Farmer.Builders


module Vm1 =
    let rec vnet1 vmName =
        vnet {
            name (nameof vnet1)

            build_address_spaces [
                addressSpace {
                    space "10.28.0.0/16"

                    subnets [
                        buildSubnet $"{vmName}-subnet" 26
                        buildSubnet "GatewaySubnet" 28
                        buildSubnet "AzureBastionSubnet" 29
                        //                        buildSubnetDelegations
//                            "containers"
//                            27
//                            [
//                                SubnetDelegationService.ContainerGroups
//                            ]
                        ]
                }
            ]
        }

    let rec vm1 =
        let scriptUrl = "https://fc1943s.github.io/mold/mold-install-windows.ps1"

        vm {
            name (nameof vm1)
            username (nameof vm1)
            vm_size Vm.Standard_D2_v3
            operating_system Vm.Windows10Pro
            os_disk 128 Vm.StandardSSD_LRS
            link_to_vnet (vnet1 (nameof vm1))

            custom_script (
                " powershell \" & { "
                + "$f = Join-Path $env:USERPROFILE 'mold-install-windows.ps1'; "
                + $"irm {scriptUrl}?t={System.DateTime.UtcNow.Ticks} > $f; "
                + $"& $f -username {nameof vm1}; }} \" "
            )
        }

    let rec bastion1 =
        bastion {
            name (nameof bastion1)
            vnet (nameof vnet1)
        }

    let deployment =
        arm {
            location Location.BrazilSouth

            add_resources [
                vm1
                vnet1 (nameof vm1)
                bastion1
            ]
        }

module Program =
    [<EntryPoint>]
    let main _ =
        //printf "Generating ARM template..."
        //Vm1.deployment |> Writer.quickWrite "output"
        //printfn "all done! Template written to output.json"

        Vm1.deployment
        |> Deploy.execute
            (nameof Vm1)
            [
                $"password-for-{nameof Vm1.vm1}", System.Environment.GetEnvironmentVariable "MOLD_PASSWORD_FOR_VM1"
            ]
        |> printfn "%A"

        0
