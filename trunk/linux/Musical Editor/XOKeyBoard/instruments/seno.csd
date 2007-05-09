<CsoundSynthesizer>
<CsOptions>
-odac -d -+rtaudio=alsa
</CsOptions>
<CsInstruments>
; Inicializa as variáveis globais.
sr = 44100
kr = 4410
ksmps = 10
nchnls = 1
; Instrumento #1.
instr 1
  ; Amplitude do sinal
  kamp = 30000
  ; Frequência
  kcps chnget "freq"
  ;kcps = 200
  ; Número da f-table.
  ifn = 1
  ; Toca com amplitude 30000 e frequência de 440 Hz a onda do seno
  ; armazenada na tabela 1.
  a1 oscil kamp, kcps, ifn
  ; Manda o som armazenado em a1 para o arquivo de saída, seno.wav 
  out a1
endin
</CsInstruments>
<CsScore>
; Tabela #1: uma simples onda de seno usando GEN10.
f 1 0 16384 10 1
; Toca o instrumento #1 por 120 segundos, começando em 0 segundo 
i 1 0 120
e
</CsScore>
</CsoundSynthesizer> 
