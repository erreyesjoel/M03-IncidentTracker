#!/bin/bash

# Variables de l'entorn d'auditoria per a Appium 2.0
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export ANDROID_HOME=$HOME/Android/Sdk

# Actualitzem el PATH per incloure les eines de l'SDK
export PATH=$PATH:$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/latest/bin

echo "✅ Entorn Appium carregat correctament."
echo "JAVA_HOME: $JAVA_HOME"
echo "ANDROID_HOME: $ANDROID_HOME"
