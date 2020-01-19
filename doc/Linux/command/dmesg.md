## [dmesg](https://blog.csdn.net/qq_35718410/article/details/53780226)

功能说明：显示开机信息。

语　　法：dmesg [-cn][-s <缓冲区大小>]

补充说明：kernel会将开机信息存储在ring buffer中。您若是开机时来不及查看信息，可利用dmesg来查看。开机信息亦保存在/var/log目录中，名称为dmesg的文件里。

参　　数：
　-c 　显示信息后，清除ring buffer中的内容。 
　-s<缓冲区大小> 　预设置为8196，刚好等于ring buffer的大小。 
　-n 　设置记录信息的层级。

扩展阅读一:dmesg命令主要用途

 

主要应用：

dmesg用来显示内核环缓冲区（kernel-ring buffer）内容，内核将各种消息存放在这里。在系统引导时，内核将与硬件和模块初始化相关的信息填到这个缓冲区中。内核环缓冲区中的消息对于诊断系统问题 通常非常有用。在运行dmesg时，它显示大量信息。通常通过less或grep使用管道查看dmesg的输出，这样可以更容易找到待查信息。例如，如果发现硬盘性能低下，可以使用dmesg来检查它们是否运行在DMA模式：

$dmesg | grep DMA
...
ide0: BM-DMA at 0xf000-0xf007, BIOS settings: hda:DMA, hdb:DMA
ide1: BM-DMA at 0xf008-0xf00f, BIOS settings: hdc:DMA, hdd:DMA
...

上面几行可以说明每个IDE设备正在什么模式下运行。如果以太网连接出现问题，那么可以在dmesg日志中搜索eth：

$dmesg | grep eth
forcedeth.c: Reverse Engineered nForce
ethernet driver. Version 0.49.
eth0: forcedeth.c: subsystem: 0147b:1c00
bound to 0000:00:04.0
eth0: no IPv6 routers present

如果一切正常，那么dmesg显示每个网卡的硬件配置信息。如果某项系统服务未能得到正确的配置，dmesg日志很快就填满错误消息，这是诊断故障的良好起点。

还可以用来探测系统内核模块的加载情况，比如要检测ACPI的加载情况，使用dmesg | grep acpi

 dmesg |egrep -i ''(apm|acpi)'' 

  Kernel command line: vga=274 quiet console=ttyS3,9600acpi=no-idleoot=/dev/hda3 

  ACPI: Core Subsystem version [20010208]  

  ACPI: Subsystem enabled  

  ACPI: System firmware supports: C2  

  ACPI: plvl2lat=99 plvl3lat=1001 

  ACPI: C2 enter=1417 C2 exit=354 

  ACPI: C3 enter=-1 C3 exit=-1 

  ACPI: Not using ACPI idle 

  ACPI: System firmware supports: S0 S1 S4 S5

扩展阅读二：dmesg命令使用示例

 

使用示例
示例一 将开机信息发邮件
man dmesg 写道
The program helps users to print out their bootup messages. Instead of copying the messages by hand, the user need only:
dmesg > boot.messages
and mail the boot.messages file to whoever can debug their problem.
 

[root@new55 ~]# dmesg >boot.messages

[root@new55 ~]# ls -l boot.messages 
-rw-r--r-- 1 root root 15838 12-09 12 begin_of_the_skype_highlighting 15838 12-09 12 免费  end_of_the_skype_highlighting:55 boot.messages

[root@new55 ~]# mail -s "Boot Log of Linux Server" public@web3q.net <boot.messages 
[root@new55 ~]#

示例二 浏览dmesg输出的信息
[root@new55 ~]# uname -a
Linux new55 2.6.18-194.el5 #1 SMP Tue Mar 16 21:52:43 EDT 2010 i686 i686 i386 GNU/Linux

[root@new55 ~]# dmesg | less
Linux version 2.6.18-194.el5 (mockbuild@x86-007.build.bos.redhat.com) (gcc version 4.1.2 20080704 (Red Hat 4.1.2-48)) #1 SMP Tue Mar 16 21:52:43 EDT 2010
BIOS-provided physical RAM map:
 BIOS-e820: 0000000000010000 - 000000000009fc00 (usable)
 BIOS-e820: 000000000009fc00 - 00000000000a0000 (reserved)
 BIOS-e820: 00000000000e0000 - 0000000000100000 (reserved)
 BIOS-e820: 0000000000100000 - 000000001f7d0000 (usable)
 BIOS-e820: 000000001f7d0000 - 000000001f7efc00 (reserved)
 BIOS-e820: 000000001f7efc00 - 000000001f7fb000 (ACPI NVS)
 BIOS-e820: 000000001f7fb000 - 000000001f800000 (reserved)
 BIOS-e820: 00000000e0000000 - 00000000f0000000 (reserved)
 BIOS-e820: 00000000fec00000 - 00000000fec02000 (reserved)
 BIOS-e820: 00000000fed20000 - 00000000fed9b000 (reserved)
 BIOS-e820: 00000000feda0000 - 00000000fedc0000 (reserved)
 BIOS-e820: 00000000ffb00000 - 00000000ffc00000 (reserved)
 BIOS-e820: 00000000fff00000 - 0000000100000000 (reserved)
0MB HIGHMEM available.
503MB LOWMEM available.
Memory for crash kernel (0x0 to 0x0) notwithin permissible range
disabling kdump
Using x86 segment limits to approximate NX protection
On node 0 totalpages: 128976
  DMA zone: 4096 pages, LIFO batch:0
  Normal zone: 124880 pages, LIFO batch:31
DMI 2.3 present.
Using APIC driver default
ACPI: RSDP (v000 HP                                    ) @ 0x000fe270
ACPI: RSDT (v001 HP     30C4     0x31100620 HP   0x00000001) @ 0x1f7efc84
ACPI: FADT (v002 HP     30C4     0x00000002 HP   0x00000001) @ 0x1f7efc00
ACPI: MADT (v001 HP     30C4     0x00000001 HP   0x00000001) @ 0x1f7efcb8
ACPI: MCFG (v001 HP     30C4     0x00000001 HP   0x00000001) @ 0x1f7efd14
ACPI: SSDT (v001 HP       HPQPpc 0x00001001 MSFT 0x0100000e) @ 0x1f7f6698
ACPI: DSDT (v001 HP       DAU00  0x00010000 MSFT 0x0100000e) @ 0x00000000
ACPI: PM-Timer IO Port: 0x1008
ACPI: Local APIC address 0xfec01000
ACPI: LAPIC (acpi_id[0x01] lapic_id[0x00] enabled)
Processor #0 6:13 APIC version 20
ACPI: LAPIC_NMI (acpi_id[0x01] high edge lint[0x1])
ACPI: IOAPIC (id[0x01] address[0xfec00000] gsi_base[0])
IOAPIC[0]: apic_id 1, version 32, address 0xfec00000, GSI 0-23
:

 

示例三 查看dmesg尾部的信息
[root@new55 ~]# dmesg | tail
Bluetooth: L2CAP ver 2.8
Bluetooth: L2CAP socket layer initialized
Bluetooth: RFCOMM socket layer initialized
Bluetooth: RFCOMM TTY layer initialized
Bluetooth: RFCOMM ver 1.8
Bluetooth: HIDP (Human Interface Emulation) ver 1.1
eth0: no IPv6 routers present
Installing knfsd (copyright (C) 1996 okir@monad.swb.de).
NFSD: Using /var/lib/nfs/v4recovery as the NFSv4 state recovery directory
NFSD: starting 90-second grace period
[root@new55 ~]#

 

示例四 安装SS7卡驱动时的内核日志
[root@localhost ss7dpklnx]# cd SS7HD_DRIVER/
[root@localhost SS7HD_DRIVER]# ls
bbdddlnx_iss.h  bbd_hbi.h  bbd_ioc.c  bbd_isr.c  bbd_pci.c  BSD_license.txt  GPL_V2-only_license.txt  install_ss7hd.sh  Makefile26
bbd_def.h       bbd_hs.c   bbd_ioc.h  bbd_lnx.c  bbd_pro.h  build_ss7hd.sh   i21555.h                 Makefile24
[root@localhost SS7HD_DRIVER]# ./build_ss7hd.sh 
make: Entering directory `/usr/src/kernels/2.6.9-22.EL-i686'
  CC [M]  /root/setup/ss7dpklnx/SS7HD_DRIVER/bbd_hs.o
  CC [M]  /root/setup/ss7dpklnx/SS7HD_DRIVER/bbd_ioc.o
  CC [M]  /root/setup/ss7dpklnx/SS7HD_DRIVER/bbd_isr.o
  CC [M]  /root/setup/ss7dpklnx/SS7HD_DRIVER/bbd_pci.o
  CC [M]  /root/setup/ss7dpklnx/SS7HD_DRIVER/bbd_lnx.o
  LD [M]  /root/setup/ss7dpklnx/SS7HD_DRIVER/ss7hddvr26.o
  Building modules, stage 2.
  MODPOST
  CC      /root/setup/ss7dpklnx/SS7HD_DRIVER/ss7hddvr26.mod.o
  LD [M]  /root/setup/ss7dpklnx/SS7HD_DRIVER/ss7hddvr26.ko
make: Leaving directory `/usr/src/kernels/2.6.9-22.EL-i686'http://www.linuxso.com/command/dmesg.html

[root@localhost SS7HD_DRIVER]# ./install_ss7hd.sh 
[root@localhost SS7HD_DRIVER]# lsmod | grep ss7
ss7hddvr26             25808  0
[root@localhost SS7HD_DRIVER]# dmesg | tail
ACPI: PCI interrupt 0000:02:0d.0[?] -> GSI 9 (level, low) -> IRQ 9
BBD[0] 64bit
SS7HD[0] - suspend


Dialogic SS7HD Device Driver V100.00 (Source V1.21)
Copyright (C) Dialogic Corporation 2003-2010.  All Rights Reserved
Using major device number 251.
ACPI: PCI interrupt 0000:02:0d.0[?] -> GSI 9 (level, low) -> IRQ 9
BBD[0] 64bit
[root@localhost SS7HD_DRIVER]# ./install_ss7hd.sh remove
[root@localhost SS7HD_DRIVER]# lsmod | grep ss7
[root@localhost SS7HD_DRIVER]# dmesg | tail
BBD[0] 64bit
SS7HD[0] - suspend


Dialogic SS7HD Device Driver V100.00 (Source V1.21)
Copyright (C) Dialogic Corporation 2003-2010.  All Rights Reserved
Using major device number 251.
ACPI: PCI interrupt 0000:02:0d.0[?] -> GSI 9 (level, low) -> IRQ 9
BBD[0] 64bit
SS7HD[0] - suspend
[root@localhost SS7HD_DRIVER]#

 

示例五 打印并清除内核环形缓冲区
[root@new55 ~]# dmesg -c
Linux version 2.6.18-194.el5 (mockbuild@x86-007.build.bos.redhat.com) (gcc version 4.1.2 20080704 (Red Hat 4.1.2-48)) #1 SMP Tue Mar 16 21:52:43 EDT 2010
BIOS-provided physical RAM map:
 BIOS-e820: 0000000000010000 - 000000000009fc00 (usable)
 BIOS-e820: 000000000009fc00 - 00000000000a0000 (reserved)
 BIOS-e820: 00000000000e0000 - 0000000000100000 (reserved)
 BIOS-e820: 0000000000100000 - 000000001f7d0000 (usable)
 BIOS-e820: 000000001f7d0000 - 000000001f7efc00 (reserved)
 BIOS-e820: 000000001f7efc00 - 000000001f7fb000 (ACPI NVS)
 BIOS-e820: 000000001f7fb000 - 000000001f800000 (reserved)
 BIOS-e820: 00000000e0000000 - 00000000f0000000 (reserved)
 BIOS-e820: 00000000fec00000 - 00000000fec02000 (reserved)
 BIOS-e820: 00000000fed20000 - 00000000fed9b000 (reserved)
 BIOS-e820: 00000000feda0000 - 00000000fedc0000 (reserved)
 BIOS-e820: 00000000ffb00000 - 00000000ffc00000 (reserved)
 BIOS-e820: 00000000fff00000 - 0000000100000000 (reserved)
0MB HIGHMEM available.
503MB LOWMEM available.
Memory for crash kernel (0x0 to 0x0) notwithin permissible range
disabling kdump
Using x86 segment limits to approximate NX protection
On node 0 totalpages: 128976
  DMA zone: 4096 pages, LIFO batch:0
  Normal zone: 124880 pages, LIFO batch:31
DMI 2.3 present.

省略输出

Bluetooth: HIDP (Human Interface Emulation) ver 1.1
eth0: no IPv6 routers present
Installing knfsd (copyright (C) 1996 okir@monad.swb.de).
NFSD: Using /var/lib/nfs/v4recovery as the NFSv4 state recovery directory
NFSD: starting 90-second grace period
[root@new55 ~]# dmesg

[root@new55 ~]# less /var/log/dmesg
Linux version 2.6.18-194.el5 (mockbuild@x86-007.build.bos.redhat.com) (gcc version 4.1.2 20080704 (Red Hat 4.1.2-48)) #1 SMP Tue Mar 16 21:52:43 EDT 2010
BIOS-provided physical RAM map:
 BIOS-e820: 0000000000010000 - 000000000009fc00 (usable)
 BIOS-e820: 000000000009fc00 - 00000000000a0000 (reserved)
 BIOS-e820: 00000000000e0000 - 0000000000100000 (reserved)
 BIOS-e820: 0000000000100000 - 000000001f7d0000 (usable)
 BIOS-e820: 000000001f7d0000 - 000000001f7efc00 (reserved)
 BIOS-e820: 000000001f7efc00 - 000000001f7fb000 (ACPI NVS)
 BIOS-e820: 000000001f7fb000 - 000000001f800000 (reserved)
 BIOS-e820: 00000000e0000000 - 00000000f0000000 (reserved)
 BIOS-e820: 00000000fec00000 - 00000000fec02000 (reserved)
 BIOS-e820: 00000000fed20000 - 00000000fed9b000 (reserved)
 BIOS-e820: 00000000feda0000 - 00000000fedc0000 (reserved)
 BIOS-e820: 00000000ffb00000 - 00000000ffc00000 (reserved)
 BIOS-e820: 00000000fff00000 - 0000000100000000 (reserved)
0MB HIGHMEM available.
503MB LOWMEM available.
Memory for crash kernel (0x0 to 0x0) notwithin permissible range
disabling kdump
Using x86 segment limits to approximate NX protection
On node 0 totalpages: 128976
  DMA zone: 4096 pages, LIFO batch:0
  Normal zone: 124880 pages, LIFO batch:31
DMI 2.3 present.
Using APIC driver default
ACPI: RSDP (v000 HP                                    ) @ 0x000fe270
ACPI: RSDT (v001 HP     30C4     0x31100620 HP   0x00000001) @ 0x1f7efc84
ACPI: FADT (v002 HP     30C4     0x00000002 HP   0x00000001) @ 0x1f7efc00
ACPI: MADT (v001 HP     30C4     0x00000001 HP   0x00000001) @ 0x1f7efcb8
ACPI: MCFG (v001 HP     30C4     0x00000001 HP   0x00000001) @ 0x1f7efd14
ACPI: SSDT (v001 HP       HPQPpc 0x00001001 MSFT 0x0100000e) @ 0x1f7f6698
ACPI: DSDT (v001 HP       DAU00  0x00010000 MSFT 0x0100000e) @ 0x00000000
ACPI: PM-Timer IO Port: 0x1008
ACPI: Local APIC address 0xfec01000
ACPI: LAPIC (acpi_id[0x01] lapic_id[0x00] enabled)
Processor #0 6:13 APIC version 20
ACPI: LAPIC_NMI (acpi_id[0x01] high edge lint[0x1])
ACPI: IOAPIC (id[0x01] address[0xfec00000] gsi_base[0])
IOAPIC[0]: apic_id 1, version 32, address 0xfec00000, GSI 0-23
[root@new55 ~]#

http://www.linuxso.com/command/dmesg.html