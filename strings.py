musings = [
    "Know no want.",
    "To wait for tomorrow is for fools in their sorrow.",
    "The memory fades and I weaken.",
    "Wit is the salt of conversation, not the food.",
    "By any means necessary.",
    "I struck a match against the door.",
    "What is today but ereyesterday's postmorrow?",
    "What is better - to be born good, or to overcome your evil nature through great effort?",
    "Violence now, that there may be peace later."
]

controls = r"""numpad - movement and attack.

 ┌  ^  ┐
  7 8 9
 <4   6>
  1 2 3
 └  v  ┘

l look mode - navigate with the numpad or mouse
i view inventory / use something / equip something
g get item
> descend stairs

. wait (i.e, pass your turn)
d drop item
c view character sheet
m view detailed message log

b   edit binds
1-9 use binds
"""

general_info = r"""
the goal of this game is to eat fucking shit and die
"""

about = r"""
Thank you for playing The Stars Came Down Screaming! Or as my girlfriend lovingly calls it, TSCDS.
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
