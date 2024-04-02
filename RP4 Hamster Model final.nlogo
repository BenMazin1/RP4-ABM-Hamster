turtles-own
  [chemo?
  tumor-size
  tumor-days
  tumor-prechemo
  body-size
]

globals
  [ %infected
  %on-chemo
  mri-status
]


to setup
  clear-all
  setup-turtles
  update-global-variables
  update-display
  reset-ticks
  set mri-status 0
end

to setup-turtles
  create-turtles inital-hamsters
    [ setxy random-xcor random-ycor
      set size 2.7
      get-healthy
      set shape "hamster"
      set body-size 1500000 + random 2000000  ;;min +  random (max-min)
  ]
  ask n-of inital_cancer turtles
    [ set tumor-size 1
  set tumor-days 5 ]
end


to get-healthy
  set tumor-size 0
  set tumor-prechemo 0
  set chemo? false
end

to move ;; turtle procedure
  rt random 100
  lt random 100
  fd 1
end

to infect
  let first-hamster-tumor-size tumor-size ;; so as to not get confused w other hamster
  ask other turtles-here with [tumor-size < 1 and not chemo?]
      [if random-float 100 < infectiousness
         [ set tumor-size 1 ] ]
end

to MRI
  if chemo-work [ if tumor-size > 0 [ set chemo? true set tumor-prechemo tumor-size ]]
  if chemo? [
    if tumor-size < 0.01 [get-healthy]] ;; get off chemo and assume healthy when tumor is super small
end

to tumor-grow
  ;; assuming shrinking rate includes growth rate in it!
  if chemo? = false [
    if tumor-days > 4 [
      set tumor-size (0.4574 * (tumor-days - 4) ^ 3 - 4.9283 * (tumor-days - 4) ^ 2 + 22.188 * (tumor-days - 4))]]
      ;; this equation found on excel through data approxtimations and line of best fit w R^2 value 0.9966
end

to tumor-shrink
  set tumor-size tumor-size - tumor-prechemo * 0.05
  ;; 68% reduction in 14 days from article ~ 5% reduction rate every day
  ;; set as function of original tumor size when chemo began
end

to update-global-variables
  if count turtles > 0
    [ set %infected (count turtles with [ tumor-size > 0 ] / count turtles) * 100
      set %on-chemo (count turtles with [ chemo? ] / count turtles) * 100
      ]
end

to update-display
  ask turtles
    [ set color ifelse-value tumor-size > 0 [ ifelse-value chemo? [blue] [red] ] [ green ] ]
end

to go
  ask turtles [
    move
    if mri-status = MRI-frequency [
      MRI
    ]
    if tumor-size > 0[
      infect
      set tumor-days tumor-days + 1
      if (tumor-size / body-size) > death-threshold [die]
      if tumor-days > 4 [tumor-grow] ;; latent period!
      if chemo? [tumor-shrink]
    ]
  ]
  update-global-variables
  update-display
  if mri-status = MRI-frequency [
      set mri-status 0
    ]
  set mri-status mri-status + 1
  if %infected = 0 [
    export-plot "Populations" (word "/Users/benmazin/Code Dev/RP 4/output ABM/world" behaviorspace-run-number ".csv")
    stop
    ]
  tick
end
@#$#@#$#@
GRAPHICS-WINDOW
280
10
778
509
-1
-1
14.0
1
10
1
1
1
0
1
1
1
-17
17
-17
17
1
1
1
ticks
30.0

SLIDER
5
145
140
178
infectiousness
infectiousness
0.0
100
60.0
1.0
1
NIL
HORIZONTAL

BUTTON
155
275
265
350
NIL
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
0

PLOT
15
440
267
604
Populations
days
hamsters
0.0
60.0
0.0
100.0
true
true
"" ""
PENS
"sick" 1.0 0 -2674135 true "" "plot count turtles with [ tumor-size > 0.1 ]"
"healthy" 1.0 0 -10899396 true "" "plot count turtles with [ tumor-size < 0.1 ]"
"total" 1.0 0 -1184463 true "" "plot count turtles"
"on chemo" 1.0 0 -14070903 true "" "plot count turtles with [ chemo? ]"

MONITOR
15
395
80
440
NIL
%infected
1
1
11

MONITOR
155
395
205
440
days
ticks
1
1
11

SLIDER
115
40
275
73
inital_cancer
inital_cancer
0
inital-hamsters
25.0
1
1
NIL
HORIZONTAL

MONITOR
90
395
145
440
%chemo
%on-chemo
1
1
11

SLIDER
115
75
275
108
MRI-frequency
MRI-frequency
1
30
7.0
1
1
days
HORIZONTAL

SLIDER
5
180
182
213
death-threshold
death-threshold
0.001
0.005
0.004
0.0001
1
%
HORIZONTAL

BUTTON
15
275
140
308
NIL
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

INPUTBOX
5
40
110
100
inital-hamsters
100.0
1
0
Number

TEXTBOX
90
10
240
35
Study Setup
15
0.0
1

TEXTBOX
90
120
240
138
Cancer Traits
15
0.0
1

TEXTBOX
115
245
265
263
Control
15
0.0
1

MONITOR
217
395
267
440
Dead
inital-hamsters - count turtles
0
1
11

TEXTBOX
120
365
270
390
Output
15
0.0
1

SWITCH
15
315
140
348
chemo-work
chemo-work
0
1
-1000

@#$#@#$#@
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

hamster
false
0
Polygon -7500403 true true 289 142 271 165 237 164 217 185 235 192 254 192 259 199 245 200 248 203 226 199 200 194 155 195 122 185 84 187 91 195 82 192 83 201 72 190 67 199 62 185 46 183 36 165 40 134 57 115 74 106 60 109 90 97 112 94 92 93 130 86 154 88 134 81 183 90 197 94 183 86 212 95 211 88 224 83 235 88 248 97 246 90 257 107 255 97 270 120
Polygon -16777216 true false 234 100 220 96 210 100 214 111 228 116 239 115
Circle -16777216 true false 246 117 20
Line -7500403 true 270 153 282 174
Line -7500403 true 272 153 255 173
Line -7500403 true 269 156 268 177

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.4.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
<experiments>
  <experiment name="experiment" repetitions="200000" sequentialRunOrder="false" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <enumeratedValueSet variable="inital_cancer">
      <value value="25"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="death-threshold">
      <value value="0.004"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="infectiousness">
      <value value="60"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="chemo-work">
      <value value="false"/>
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="MRI-frequency">
      <value value="7"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="inital-hamsters">
      <value value="100"/>
    </enumeratedValueSet>
  </experiment>
</experiments>
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
1
@#$#@#$#@
