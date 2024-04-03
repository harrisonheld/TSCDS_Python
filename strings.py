controls = r"""Movement and Attack - use the numpad.
┌  ^  ┐
 7 8 9
<4   6>
 1 2 3
└  v  ┘

Controls
l - look
g - get item
d - drop item
i - view inventory
c - view character sheet
m - view detailed message log
> - descend stairs
"""

eye_art = r"""*{##<^<><[}<))))())))))))))(]]](}]]}{}[(]{[]{}}[[}{[#{[(([[]]][(]<]{#@@{[][[}}{]([{-~<<(*:-..........--.........(...........................................:~^###%%#
:[.[@@{#%##@@@###%%%%%@%@@%%@@##@@%%%%@%@%%#@%%%##@%%@@@@@#%@@%@[{}(>>[@@@@%[[}^-:=%#[==]@@^+(#[[}>~>-.*@@...<:..{>%@@@]~(@[..+)<+::~~-:+====++~=~==~===*^)]##%@@@@@%
:+-..%@@@#{#{#@@@#%%%@@%%%#%%%%%%#####%%#@@%%%@@@@@#%%%#@@@@@%#@@@@@@{<..:@@@@@@@@{::^#@(::>+==:-)>+:-:<>]#@%..-=+.<..-%%#^:..:::=*^----:---==~:~~-=:==^<)(]{{#@@@@@%
<@@@@<%@@%@@@@@@%%%%@}#@%%%%%%@}@@@@@#@@%%#%##%@###@{%@%}(+[*()--*@@@%@@@=...>@@@@%#%]{:...:*~>))(](+.:......::*@[<{...<#}=~=^^-:::::::::-:--:::..:.--**>>)({{{@@%%@%
.....+@@%#%@%@@@@%%@@###%@@@@@%#{%%%##%@@%%@%%%}#%%%@%#%@@@@@{#{[+..-=+]@@@@.^^>}@@@@@%<>](@@{#=.-<#@^~=:.:>..::....~[{)-.=()>^~:^)>>=-::::--~--++~~+**+~<)({#@@@@@@@
.]#~.{@#{#%%%@#%@%%@@%@@@}[}{@%@@%#%%@@##%#%#%%@%%}{{{#####@@@%@#{}):.....:%@@>)]]:%@@@@[+.:-=]#)...-<(<-~:......^+.:=+:...........-<<+~-~:::--..:.:....-<)){}@@@@@@%
....{@@@@@@@@@{%%{#####@@@@@[#%%{%@%]{#%@@@%%%##%%%%%#%]}[]][{[{%@@@%@@@}^~...==-=~:...@@@@~{)>{#*:..-.--:-~~)[^=*<>*+^}}>~:==++*~*++=*~:--==~:....::^))](((}{@@@%%%#
.::^@@{@%@@}#{##%@@%##%@@%#%@%%%#}%%@%#####%%%@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@(~....=~}@=..+@@@^:.):-=::<^.:..:+*=:+]](-...>+~--:.~*+:^][>+:::-~:---===+*+)))(}#%@@%@@@
...@@%#@%%%###{#%#{%%%{{#%{#%##%@%@@%%%%@@@%%##[[}##%%%))#%%%%}@@@@@%@@@@@@@%@@{):....>{^....{@@%.-..+=::-:...:+<*:~:-<~)[})~.:~^+--:>)^~-::::-:~~*=+<^^)>)[[{#@@%@@%
..@@{@@@%%}@@%%[{}@@@%#@@{#%%#{}{{{{{{{{([}{#@@@@@@@}{{@@%{}]#}(]][[}[}{#[%@@@@@@{{{=...~}]@{...+@%#]~*>->->#*.-{#]>+=-.^([(=.=(<^=+^*+=^-:-:-:::::::=~>(<<]]{#@@%@@%
.+@@@%%%@@%###%#%{#%%%%%%##%%%@@@@@@@@@@@@@@@@%@@%#{@@@@@{@@@@@@@@@@@%%{}}[*:.-@@@@@@@[*....}@@...~@[:......:>>:..=)#}}[}])(((<:.~~~.:+~(><*...:::=-~+~:<)([}{@@@@@@@
.)@%@@@@##%%%#####{}{##%%%##{@%{{%%%#@@@%@%{}}{%%#{@%###%%=~)%@#{{%%%@%[][###]^:..^@@@@}()~...@@}-..~@-....:~~~++-.:=**::-+<(<***+<^*+=-~~^^+=-::::::-*+>)(][{%@@%@%%
.@@@@%@@{#%###{##{{@%###%@%@@%%%#@@@@@@@%[]}%@@##%%%@@@@@@@@@@@@@@@@@@@@@@@@@@#}##*...@@@%%@{:..-{[~..-~~-.::......-+<>:.:-**~:-^**-=++:*-*=::......::~~+><([%%@@%@@%
.@@@@@@@{{#{%%%#@%#%#%%%@%#%%#@@@%%%#{{}}%@@@%%{@@@@@@@}}}{}{{}#{{#%#@%@@@@@@@@@@@%}(:.=.#@%})=....[):.]-....::--=+*>**>^^+=+~++.:~:*+=>(^*=.::.::--+>^^<]}}#%@@@@@@%
.@%{@@@@@@@%@%#{##@%%@%%%##@@@@#%####}#%}@%}%@@@@%#{#{{%%@@@@%#@@@%@@{%%%%##@@[[%@@@@@@@{^{@@%}<:....+-.{}~:--::.:=+<^=:-~==+=^>=*^>+~^*^>*=.-=~~:.::=*+>)]{#{%@@@@%#
.@@@%%%%##%%%%#@%##{##@%@@@@@%#{[%%%{#@@@@@@@@%{}{{#{{%#{##{##%#%#{%%%%%%%%##%#@[{#@%(@#%@%{#@@@#=-*....:[^....:.....-)))<<~~-~=+=^*~==+<>*~=:~---=-=**><[(}{%@@@@@@#
:@@@@@%%%#%%%%##%##@@%@%%%@@[[#%%%#%@@@@@@%#%@@%%@@@@#}{{{{{##{%#{###%%%%%%%%@@@@%#}%@@[@@@@@@{{%@@%]}~....^<~.:-~==<<*~-==*~===*>^^+-:-~+~:-:::..:=+^*>)](}#@@@@@@@#
-@@%@@%%##%##%{{##{##{@%@}#{[%%#{@@@@%@@%}}[([}#[}])}}}}{{}}{{{##{%###########{#{{##%{%@{@}%#@@@@@##{[^+~:...~---:-*[(^>>>>)>**^+^*^*^::.:--.:::::=-=^^>([]{#@@@@@@@#
:@@@{{%@%#%%##%@@%#%%%##%%#%%@%@@%@@@@@@{%@}{{[(<([}#{}#{##{###{#%@{{%%%##{}[{%#@@@@%@@%@#{@}@@@}^@{}<#@)=--..~*==~--==*^*)*~::::~~-+==^~~=+-~-~~==~+^^<([[{#%@@@%@@#
.%%%@@@%%@@#@@@%%%%@%@###@%@@%@@@#@%{%%}{}{%[}{#]##]##%##{#{###@@%@@%#%%#{%%@@@@@@@%@@@%@@@%@@%@@@#<@@@*<^~:...::~~~=++=~+~....--::-~+*^^>==:~-=~-==+^><(}}#%@@@@@@@#
.@@@@@@#@%%#%##%%#{#{#%%%@#@@#@%@{%@%%@%%[{{)][@%#^({{{{{##{##%#{{{%%@@%[}@@%@%#{(}#@@@%@%@@@@%%@@@@%]@%)}]^--:..:-+*<*++=^----=---:=====^==::.:::-~=*>))}[{@@@%%%@@#
.@@#%@@@@%@@%%%%{{#@@@@@@@%%@@%%@@(>%@#[{]}{}#@}.@@%@##@%#####%#%%#@@{{{{@@@@@{{{%()~]@@@@@%#%%%#@@@@+#@#{^^.:--~::~+*--~=*-=--=:.~:+===~~-:~~-::.-=+*<))[]{%@@@@@@@#
.@@@@@@@@@@%%%{@@@@@@@@@@@@@@@[@%%[@@%[}%###{[({)@@{@%#}}{{{{{#{{{{{{{{%@@@@}}}%@@@@%]+...@@@@%%%@@%+%@]>#{^..:::-+-^<^*+*++*^*=~~+=~~~---:-:-:::.-=+*<(]}{%@@@@@@@@#
.@@@%%%%%%###%%%@@@}%@#####%#%##%%]#@%{#{[][}^<{{]^-{}}}}{}#{[###][}}{{##{*)}%##%@%@@@@=..-@@@%%%%@#<@@<)%[(==:=-+=~:~~==**==***======~.:--~---~~=+=+*)][}}##@@@%%@@#
.@@#%%%@#%@@@@%@@@@%%{#%%%%@@@@@%#}@%[{@[[}#}{}%{}%#@{{{}}][{%{###%%@##%@%}[@@@%@@@%%@@@@@~>@@@%%%@@%@@{<#[>~:-~-+==++-:-++=.--=:~~----=-~--:.:++^++>>])]{#{@@@@@@@@#
.>@@%%%@###@%%@@@@@@@@%@@@%@@%@@%#}@@[}{[#}=}<#@%#{{[]%}@@@@%%%{}#%#%{{}@>)@@@@@@%@@@@@@@@%:^@@%%%@@@@@{}([]^~::--==+<+=++>^<>~~~------=:-:::-.-=*)[[[]([##%@%@@@@@@%
..@@@@@@%%#@@%#@%#}@@@@@@@%@@#%%%}]%@%%[}[{}[{).:{}){@%%{]]]}{[<}}{{##[#+.:@@@%%%%@#@%@@@@@(){@@@%%%@@@{{]]>*-----^<>]^+==++++=~:::.-:-==~:.:.:..:....[]}{##@@@@@@@@#
...@@@@%@%%#%%%%@@#%#%%%%%%@@@@@@@@@@@@@@@%}[[[{%@@@%}[%###%#{}{}#{%%[}#>-<@@@%@@%@#@@@@@@@}(@@@@@@@@@%{{[[~~~::.:.:*))=::--~==*:~-~::-~---::.....=**:}([[%@@@@@@@@@%
....@@@[}@@%#%#{}@#@%%%%%%%%%{%@%#%%@@@@@@%@@@{{@}((([[#{#{%#@{@%@%%}]])+=+@@@@@@%@@@@@@@@@@@{@@@@@@@@@@@{#(>=---:..:=*---+**+*^^*-=:--~::.:-----~=-^)([[}@@@@@@@@@@%
.:-.:@@@@@%{#%{#}]###@@@%##{}}}{[{{[^>}@@@@@@@@@%@@%@}}[[}}#}#{%####%{[]#%)]@@@@@@@@@@#[{@@@}}[-:-:.>@@@@{[<>^*++=~==~~=*^====+^-~+*--~=~:........~*><<][{@@@@@@@@@@%
.~~..+@@%#%{#%%%@%#%%%{^@@@%%##%{}[}@]<.+.+*>([@@@@@@@@@@{}}{{{#{%{{{#{]#)-:=[@@@@@@(]]}%@]^@[++--:..#@%@#[+-~++~~-~~-::+*>^*=++*--~=++==-*-:::-~+=*><<[{##@@@@@@%@@#
.++-...@@@%{%#{}#%@@@@@@}#}{@#{#@@@@}@@%+.-)=:......:~>@@@@@@@@@@@@@{#}[(--~..-:::-+{@@@@@..--:-=....@@@@@%}^=~:-:::.::+=^<<(^>+~-~-:-:=+=-:.:::~=+=><<][{@@@@@@@@@@%
.><:-:..@@@{{}{{{#)[}(=)(%@%}%@@}:~%#[^^@@^<<)(*.-...........+))%#@@@@@@@@@@@@}{@@@@@@@@#])>^=^:...:}@@@@@@@#(<*=:...:-+=~~~+~~:-::::::++*^~---::~~~^<<[{{@@@%@@@@@@#
.=^-.-...@@@#{###{{#})+)#%}@@[}@@@@%%@@#%@#{@[%@@@#%=~:[=:.............:=(%@@@@@@]<-.....:=^*^-.>](>(%@@@@@@%@{<^+------.-::---::---:=~--~=-+**-:~*^^<)][}@@@%@@@@@@%
.:*=--==..@@@#{###{#}[@@@#}(*@@{*@@@@@@@@#@#%##@@@@@=@%%>*)###:[)~.....=<:.....*(>.~..:+=....-(^:+=:...:<@@@@#}(<^>^+~=~~::::::--~~-:-~=+.:-*+>^^>^+*><]{#@@@@@@@@@@%
.~^=:-==~..*@@%}{}#}{{{{{%#%)#{{#[%#{{##{{%@@%@%#[#@@@@@}^...-*]@]<[})=:..=-.-..:..+.)[*>@]*[*:.~........:(%@@()^>+*~--~++^^^=====~-~~~:~:--=~~-:+~+^<<]}{@@@%%@@@@@%
.~^+:--~:.:..@@@#@@%%#@]{[}%}@@@@[{@@%@}#@@@#%%#%%@%#[#[<@#@@@@@.~@@{(.*@%@%)]{%{{(]}:.<..*:^.-^+:..:--:..->@@@@<^~+~~==+=~~=*+=~-~--:-:::::::-:-=**><<][[@@@@@@@@@@%
.=-+-::-*=~:..@@@#{{{{####{{>]=*@]%%)@@%@%{%%%%%@@@{{%@@%%@@@@~+@@@+@@@@%@@@@@({{}{@%][[)):^[+>-...:-~-.....-(@@})~+**^~:~~~---::.......:::::..:.::-*<>)[}@@@@@@@@@@%
.=++~:.:+*~-...@@@#{###%##@{+{{[#}@@@@%##@@@@@@@@@%@@@%@@@@@~)@@)-~@[](@().*#@>{%@@@%#@%}}^[<....::::-......:~}#@{<^=::.:---:~~--:::::::--::::::.:-~+>^)]}%@@@@@@@@@%
.-~++:-..+~--...<@@#%%][}[%{%{%@#.~(*@%@#[[{%%{@@@@@@@@@%#{%@@@@@@@@}^*[@@@[(}->^:..~>>><}>+~:..--...::--......=<<(^-:.:::~~--::::::::.::::::..:..:=*>>][{%@@@@%%%@@#
.~:-+~:..::-+....=@@@{###[}{}][#*}{*....=%@<(}{]>.^@@@}}@@@@@@@@@@@@%@@@%()^<<*:-*<++>-:.....:-*=..--.......:--~:=~+=~:--::::--:-:::::::----~--~~==+^<<[}{%@@@@@@@@@%
.:+-=~.:::~-:......@@@@@%[@%#{@}{>*%{[})+.-==-^@@#<.:]@@@#@@%<:.@)~=*++:#@%[#[]}%@{#*-*=+^^=:......-.........::-:=)]]<*--:::::::::::::::::-:-:::::=*^>>([#@@@@@@@@@@%
.:=-~-:-:.~=--=-....@@@####{%{#%<>(%#[).:=](=^>:.(@{-...:@>@@@@@@@@@@@#@@::@{{**>-:.>%]-.:=>=::<[=-::.........:.::-=+<<++~---:---:::-:::-:=~---~-~=~+^^([##@@@@@%@@@[
.-==~+*...-.=+~>:....]@@@{{}][}@<###]>>]{)(>>=]^.~:<@}{^+..{[{-.-..^=#}}>+.=}@#]^^^)=.:::^^...^#=..:~~:......::...:-:::-=*=+~~:::::.::.::::--~-~~:::^<^)[{}%@@#%@@%%^
...---~.::-::-..+(-..:+@@%{{%{@{%@[[}}[(=<@[<*(==^+::=--@%-...~@.}@-.-^]{}[.:.-)%[>+-..+}#*..~}~...:-~...::::-............:.:::-::::-:.:-::-:-::-:*-+=><))}##}[}}}}}:
..:~~~--:--...:-..~~-...@@@%##%]##%#{>}>>=)-([<(^}~.:-^::.*%<*.:>..[=~-.:)]*::(%^^):::{[^~:..*{:..:::...::..::-:.:..........:..::::::::::..::-:-.~===*))(}[[{}[[[))<.
.:..~~~-:::-=*+^.--:..-..@##@%@@}[##@#@()*@#)[<*+[{@][[-=..+~%{+.+-.>:....^}(:#>..~--%%<-...*^:..:~~:.-:-.:::....::::::......:......::.-:::-~----:==+>><<)]]()>*=+++.
.:.~~~~-:::....~:.--:.:=.~@##@%@@@@%]-@@@<)><{<^~^<):**])(<*::...@@>..).-^-.:..:>[-+[(~+~..-}-...::.....-~~----::-::--~-~---:::::::::::-:-:----::-+*=*^^)<<)<^*+++++.
..~~:-~-::-^--:.-.:.~~....@{[#@@%#[#@@@@{]{][@%{(+}(^=~++=^-~<^....~@@@#]=..........:-.~:.*@)-.:~-.......:--~~:-~-:::....-:::-:::::.::::::-~~-:~~~~==)>>)>>**~-~~==~.
...............................-=*>==+*>)])+->=-+:...................................................................................................................
"""
