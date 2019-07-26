# sts4 (eclipse 설정) with java 12
1. Java 12버전 사용하자 
    `-vm C:\java\zulu12.2.3-ca-jdk12.0.1-win_x64\bin\javaw.exe)`
2. Java12 버전에 맞는 최신 GC를 사용하자 `-XX:+UnlockExperimentalVMOptions -XX:+UseShenandoahGC`

SpringToolSuite4.ini: 
```bash
-startup
plugins/org.eclipse.equinox.launcher_1.5.400.v20190515-0925.jar
--launcher.library
plugins/org.eclipse.equinox.launcher.win32.win32.x86_64_1.1.1000.v20190125-2016
-product
org.springframework.boot.ide.branding.sts4
--launcher.defaultAction
openFile
-vmargs
-Dosgi.requiredJavaVersion=1.8
-Xms2048m
-Xmx2048m
-XX:+UnlockExperimentalVMOptions    # 숨겨진 옵션 unlock
-XX:+UseShenandoahGC                # java12에서 지원하는 gc
-XX:+UseStringDeduplication
--add-modules=ALL-SYSTEM
-javaagent:C:\HCC_PRIVIA\sts-4.3.0.RELEASE\lombok.jar
-vm
C:\java\zulu12.2.3-ca-jdk12.0.1-win_x64\bin\javaw.exe
```

