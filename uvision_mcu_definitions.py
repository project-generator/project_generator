
def get_mcu_definition(name):
    return MCU_def[name]

MCU_def = {
    'MK20DX128xxx5' : {
        'TargetOption' : {
            'Device' : 'MK20DX128xxx5',
            'Vendor' : 'Freescale Semiconductor',
            'Cpu'    : 'IRAM(0x1FFFE000-0x1FFFFFFF) IRAM2(0x20000000-0x20001FFF) IROM(0x0-0x1FFFF) IROM2(0x10000000-0x10007FFF) CLOCK(12000000) CPUTYPE("Cortex-M4") ELITTLE',
            'FlashDriverDll' : 'ULP2CM3(-O2510 -S0 -C0 -FO15 -FD20000000 -FC800 -FN2 -FF0MK_P128_50MHZ -FS00 -FL020000 -FF1MK_D32_50MHZ -FS110000000 -FL108000)',
            'DeviceId' : 6206,
            'SFDFile' : 'SFD\Freescale\Kinetis\MK20D5.sfr',
        }
    },
    'LPC1768' : {
        'TargetOption' : {
            'Device' : 'LPC1768',
            'Vendor' : 'NXP',
            'Cpu'    : 'IRAM(0x10000000-0x10007FFF) IRAM2(0x2007C000-0x20083FFF) IROM(0-0x7FFFF) CLOCK(12000000) CPUTYPE("Cortex-M3")',
            'FlashDriverDll' : 'UL2CM3(-O463 -S0 -C0 -FO7 -FD10000000 -FC800 -FN1 -FF0LPC_IAP_512 -FS00 -FL080000)',
            'DeviceId' : 4868,
            'SFDFile' : 'SFD\NXP\LPC176x5x\LPC176x5x.SFR',
        }
    }

}
