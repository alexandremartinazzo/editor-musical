<CsoundSynthesizer>
<CsOptions>
;; RealTime audio, using the alsa module
 -odac -d -+rtaudio=alsa -b1024
</CsOptions>
<CsInstruments>
sr     = 44100
kr     = 2205
ksmps  = 20
nchnls = 1


;;
;; instrument 1  -  SENO
;;
instr 1
  kamp = 30000
  icps = p4
  ifn = 1
  a1 oscil kamp, icps, ifn
  out a1
endin

;;
;; instrument 2  -  SIMPLE DRUM
;;
instr 2
  iptch = p4
  asig pluck p5, iptch, iptch*0.81, 1, 3, .5
  out asig
endin


;;
;; instrument 3  -  ORGAN
;;
instr 3
  ifrq = p4
  
  kenv linseg 0, .01, p5, p3-.02, p4, .01, 0

  a1     oscil 8,   1      * ifrq,  1
  a2     oscil 8,   2      * ifrq,  1
  a3     oscil 8,   2.9966 * ifrq,  1
  a4     oscil 8,   4      * ifrq,  1
  a5     oscil 3,   5.9932 * ifrq,  1
  a6     oscil 2,   8      * ifrq,  1
  a7     oscil 1,  10.0794 * ifrq,  1
  a8     oscil 1,  11.9864 * ifrq,  1
  a9     oscil 4,  16      * ifrq,  1

  aorgan = kenv* (a1+a2+a3+a4+a5+a6+a7+a8+a9)

  outs aorgan
endin

;;
;; instrument 4  -  clarinet
;;
instr 4
  idur   = p3
  iamp   = p5
  ifenv  = 51                   
  ifdyn  = 52                    
  ifq1   = p4*3          
  if1    = 3                    
  ifq2   = p4*2
  if2    = 3
  imax   = 5
  imin   = 2
  
     aenv  oscili   iamp, 1/idur, ifenv                ; envelope
  
     adyn  oscili   ifq2*(imax-imin), 1/idur, ifdyn    ; index
     adyn  =        (ifq2*imin)+adyn                   ; add minimum value
     amod  oscili   adyn, ifq2, if2                    ; modulator
  
     a1    oscili   aenv, ifq1+amod, if1               ; carrier
           out      a1
endin


;;
;; instrument 5  -  hi hat
;;
instr 5

  ilen init p3
  iamp init p4

  kcutfreq  expon     10000, 0.1, 2500
  aamp      expon     iamp,  0.1,   10
  arand     rand      aamp
  alp1      butterlp  arand,kcutfreq
  alp2      butterlp  alp1,kcutfreq
  ahp1      butterhp  alp2,3500
  asigpre   butterhp  ahp1,3500
  asig      linen    (asigpre+arand/2),0,ilen, .05  

  out asig
endin
</CsInstruments>
<CsScore>
f 1  0   8192  10   1 .02 .01
f 2 0 8 2  1 1 1 1 1 -1 -1 -1

f 3  0  512  10  1
f 51 0 1024  5  .0001 200 1 674 1 150 .0001       ; amplitude envelope
f 52 0 1024  5  1 1024 .0001                      ; index envelope
;; dummy table to play for 120 secs
f 0 43200
</CsScore>
</CsoundSynthesizer> 
