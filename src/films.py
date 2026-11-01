# 作品ガイド（1作品を丸ごと解説するページ）のデータ。「映画だけ観てもすんなり理解しづらい人」向け。
# 作品を足すときは FILM_GUIDES に1件追加して `python3 src/build.py` を実行する（相関図は relations.py）。
#
# 文章はすべて自分の言葉で書く。他のサイトの文章を写さない。確かめられない話（裏話・うわさ）は書かない。
# 日本語を直したら、同じ項目の英語（_en）も直す。
#
# 各項目:
#   summary:   この作品を3行で（ネタバレなし）
#   before:    観る前に知っておくと分かりやすいこと（ネタバレなし）
#   glossary:  用語集 (用語, 説明, 用語_en, 説明_en)
#   story:     あらすじ（ネタバレあり。章ごと） (見出し, 本文, 見出し_en, 本文_en)
#   confusing: ここが分かりにくい！Q&A（ネタバレあり） (質問, 答え, 質問_en, 答え_en)
#   points:    見逃しやすいポイント・小ネタ (見出し, 本文, 見出し_en, 本文_en)
#   ending:    ラストとおまけ映像 (見出し, 本文, 見出し_en, 本文_en)
#   next:      次に観るとよい作品（titles の slug と、理由）

FILM_GUIDES = {
    "iron-man": dict(
        updated="2026-11-01",
        # ページの色（アイアンマンの赤と金）。main=見出し、deep=タイトル帯、accent=差し色、soft=タイトル帯の文字
        theme=dict(main="#b3121b", deep="#5e0a10", accent="#f2c230", soft="#f8dcc0"),
        runtime="126分", runtime_en="126 min",
        summary=[
            "兵器会社の社長トニー・スタークが、戦地で誘拐される。",
            "洞窟で鉄のスーツを作って脱出し、自分の会社の武器が悪人に使われていたと知る。",
            "アイアンマンとして戦い始めたトニーの前に、身近にいた黒幕が立ちはだかる。",
        ],
        summary_en=[
            "Tony Stark, head of a weapons company, is kidnapped in a war zone.",
            "He builds an iron suit in a cave to escape, and learns his company's weapons are in the wrong hands.",
            "As he starts fighting as Iron Man, the real villain turns out to be someone close to him.",
        ],
        before=[
            ("MCUのいちばん最初の作品です", "マーベル映画の世界（MCU）はここから始まります。ほかの作品を知らなくても、この1本だけで話が分かります。"),
            ("トニーは最初「イヤなやつ」です", "お金持ちで自信家、人の話を聞かない社長として登場します。その彼が、誘拐をきっかけに変わっていくのがこの映画の見どころです。"),
            ("胸の光る装置に注目", "トニーの胸の丸い装置（アーク・リアクター）は、命を守る装置であり、スーツの電源でもあります。最後まで物語のカギになります。"),
            ("エンドクレジットの後まで観る", "スタッフ名が流れた後に、次の作品につながる大事な場面があります。途中で止めないでください。"),
        ],
        before_en=[
            ("It's the very first MCU film", "The Marvel Cinematic Universe starts here. You don't need to know any other film to follow it."),
            ("Tony starts out as a jerk", "He's rich, cocky and doesn't listen to anyone. Watching him change after the kidnapping is the heart of the film."),
            ("Watch the glowing device in his chest", "The round device in Tony's chest, the arc reactor, keeps him alive and powers the suit. It matters until the very end."),
            ("Stay until after the credits", "An important scene that leads to later films plays after the end credits."),
        ],
        glossary=[
            ("アーク・リアクター", "トニーの胸にある、丸く青く光る小さな発電装置。爆弾のかけらが心臓に入らないよう止める電磁石の電源で、スーツのエネルギー源にもなる。もともとは会社の工場にある大きな発電装置を、トニーが小さく作り直したもの。",
             "Arc reactor", "The small, glowing blue power source in Tony's chest. It powers the magnet that keeps bomb fragments out of his heart, and also powers the suit. Tony shrank it down from the large reactor at his company's factory."),
            ("スターク・インダストリーズ", "トニーが社長を務める、アメリカ軍に兵器を売る大企業。父ハワードが作った会社。",
             "Stark Industries", "The big company Tony runs, which sells weapons to the U.S. military. His father Howard founded it."),
            ("テン・リングス", "アフガニスタンでトニーを誘拐したテロ組織。名前は「10個の指輪」という意味。MCUではこの後も何度も登場し、『シャン・チー／テン・リングスの伝説』で正体が深く描かれる。",
             "The Ten Rings", "The terrorist group that kidnaps Tony in Afghanistan. The name means \"ten rings.\" It keeps appearing in the MCU and is explored in Shang-Chi and the Legend of the Ten Rings."),
            ("ジェリコ", "トニーが冒頭で軍に売り込む新型ミサイル。テン・リングスは、これと同じものを作れとトニーに命じる。",
             "Jericho", "The new missile Tony demonstrates to the military at the start. The Ten Rings order him to build one for them."),
            ("マーク1・マーク2・マーク3", "アイアンマンのスーツの番号。マーク1は洞窟で作った灰色の試作品、マーク2は家で作った銀色の試作品、マーク3が赤と金の完成版。",
             "Mark I, II and III", "The suit numbers. Mark I is the gray prototype built in the cave, Mark II the silver test suit built at home, and Mark III the finished red-and-gold suit."),
            ("アイアンモンガー", "オバディアが、洞窟に残されたマーク1をもとに作らせた巨大なスーツ。",
             "Iron Monger", "The giant suit Obadiah has built from the Mark I left in the cave."),
            ("J.A.R.V.I.S.（ジャーヴィス）", "トニーが作った人工知能。家の管理やスーツの操作を手伝う。のちに『エイジ・オブ・ウルトロン』でヴィジョンという人物につながる。",
             "J.A.R.V.I.S.", "The AI Tony built. It runs his house and helps operate the suit. It later leads to Vision in Age of Ultron."),
            ("S.H.I.E.L.D.（シールド）", "コールソンが所属する、アメリカの秘密の組織。この映画では「戦略国土調停補強配備局」という長い名前で名乗り、最後にS.H.I.E.L.D.と呼ばれる。のちにアベンジャーズを集める組織になる。",
             "S.H.I.E.L.D.", "The secret U.S. agency Coulson works for. He introduces it by a long name, the Strategic Homeland Intervention, Enforcement and Logistics Division, and it's called S.H.I.E.L.D. by the end. It later brings the Avengers together."),
            ("グルミラ", "インセンの故郷の村。スターク社の武器を持ったテン・リングスに襲われる。",
             "Gulmira", "Yinsen's home village, attacked by the Ten Rings using Stark weapons."),
        ],
        story=[
            ("1. アフガニスタンで誘拐される",
             "兵器会社スターク・インダストリーズの社長トニー・スタークは、新型ミサイル「ジェリコ」を軍に売り込むためアフガニスタンを訪れる。その帰り道、車列が襲われ、トニーは爆発に巻き込まれて気を失う。目を覚ますと洞窟の中。同じく捕まっていた医師インセンが、トニーの胸に電磁石を付けていた。爆弾の細かいかけらが心臓に近づかないよう止めるためだ。",
             "1. Kidnapped in Afghanistan",
             "Tony Stark, CEO of Stark Industries, visits Afghanistan to pitch the new Jericho missile to the military. On the way back his convoy is attacked and he is knocked out by an explosion. He wakes up in a cave. Yinsen, a doctor held there too, has put an electromagnet in Tony's chest to keep bomb fragments from reaching his heart."),
            ("2. 洞窟でスーツを作る",
             "トニーを捕まえたのはテロ組織テン・リングス。一団を率いるラザは「ジェリコを作れ」と命じる。洞窟には自分の会社の武器がたくさん並んでいて、トニーはショックを受ける。トニーはミサイルを作るふりをして、インセンと一緒に、胸の電磁石を動かす小さな発電装置（アーク・リアクター）と、脱出用の鉄のスーツ（マーク1）をこっそり作る。",
             "2. Building a suit in the cave",
             "His captors are the Ten Rings, and Raza, who leads them, orders him to build a Jericho. The cave is full of his own company's weapons, which shocks Tony. Pretending to build the missile, he and Yinsen secretly make a small power source for the magnet, the arc reactor, and an iron suit to escape in, the Mark I."),
            ("3. インセンの犠牲と脱出",
             "スーツの起動が間に合わないと見たインセンは、時間をかせぐために飛び出し、撃たれてしまう。インセンは「命を無駄にするな」と言い残して亡くなる。トニーはスーツで武器を焼き払い、空へ飛び出すが、砂漠に落ちてスーツは壊れる。さまよっているところを、親友ローディの捜索隊に救われる。",
             "3. Yinsen's sacrifice and the escape",
             "When the suit isn't ready in time, Yinsen runs out to buy time and is shot. Before he dies he tells Tony not to waste his life. Tony burns the weapons with the suit and blasts into the sky, but crashes in the desert and the suit breaks. His best friend Rhodey's search team finds him wandering."),
            ("4. 「もう兵器は作らない」",
             "帰国したトニーは記者会見を開き、会社の兵器づくりをやめると発表する。父の代からの共同経営者オバディアは反対し、取締役会を使ってトニーを会社の仕事から外そうとする。トニーは家の工房にこもり、ジャーヴィスとロボットアームのダミーを相手に、胸の装置を改良し、新しいスーツを作り始める。",
             "4. \"No more weapons\"",
             "Back home, Tony holds a press conference and announces the company will stop making weapons. Obadiah, his father's longtime partner, objects and uses the board to push Tony out. Tony shuts himself in his workshop and, with J.A.R.V.I.S. and the robot arm Dum-E, improves his chest reactor and starts building a new suit."),
            ("5. 赤と金のスーツと、グルミラの戦い",
             "銀色の試作スーツ（マーク2）で空を飛ぶテストをすると、高い空で凍りつく問題が見つかる。そこで改良した赤と金のスーツ（マーク3）が完成する。パーティーで記者のクリスティンから、インセンの故郷グルミラでスターク社の武器が使われている写真を見せられたトニーは、スーツで現地に飛び、テン・リングスを倒して村の人々を助ける。",
             "5. The red-and-gold suit and Gulmira",
             "Test flights in the silver Mark II reveal that it ices up at high altitude, so Tony builds the improved red-and-gold Mark III. At a party, reporter Christine shows him photos of Stark weapons being used in Gulmira, Yinsen's hometown. Tony flies there in the suit, defeats the Ten Rings and saves the villagers."),
            ("6. 黒幕はオバディアだった",
             "トニーに頼まれたペッパーは、会社のコンピューターからデータを盗み出し、オバディアがテロ組織に武器を売っていたこと、そしてトニーの誘拐（もともとは暗殺）を依頼していたことを突き止める。一方オバディアは、洞窟に残っていたマーク1の残骸をテン・リングスから受け取り、ラザたちを始末する。そしてトニーの胸から発電装置を奪い、巨大なスーツ（アイアンモンガー）を動かす。",
             "6. Obadiah was behind it all",
             "At Tony's request, Pepper copies data from the company computers and learns that Obadiah has been selling weapons to terrorists and had hired them to kill Tony. Meanwhile Obadiah takes the remains of the Mark I from the Ten Rings and has Raza's men killed. He then rips the reactor out of Tony's chest and uses it to power his giant suit, Iron Monger."),
            ("7. 最後の戦い",
             "胸の装置を失って死にかけたトニーを救ったのは、ペッパーが記念に飾っていた古い装置だった（ダミーが手渡す）。トニーはペッパーとコールソンのもとへ駆けつけ、アイアンモンガーと戦う。力で負けるトニーは、ペッパーに会社の大型発電装置を暴走させるよう頼み、そのエネルギーでオバディアを倒す。",
             "7. The final battle",
             "Dying without his reactor, Tony is saved by the old one Pepper had kept as a keepsake, handed to him by Dum-E. He races to Pepper and Coulson and fights Iron Monger. Outmatched, he has Pepper overload the large reactor at the factory, and the blast takes Obadiah down."),
            ("8. 「私がアイアンマンだ」",
             "次の日の記者会見。S.H.I.E.L.D.のコールソンが用意した「アイアンマンは護衛のボディガード」という説明を読むはずだったトニーは、途中で原稿を置き、「私がアイアンマンだ」と正体を明かしてしまう。",
             "8. \"I am Iron Man\"",
             "At the next day's press conference, Tony is supposed to read Coulson's cover story that Iron Man is a bodyguard. Instead he puts the cards down and says, \"I am Iron Man.\""),
        ],
        confusing=[
            ("なぜトニーの胸は光っているの？",
             "爆弾のかけらが体の中に残っていて、心臓に届くと死んでしまうからです。胸の電磁石がかけらを引き止めていて、その電源が光っている装置（アーク・リアクター）です。だから装置を奪われると、トニーは死にかけます。",
             "Why is Tony's chest glowing?",
             "Bomb fragments are still in his body, and they would kill him if they reached his heart. A magnet in his chest holds them back, and the glowing arc reactor powers it. That's why he nearly dies when the reactor is taken."),
            ("オバディアはなぜ裏切ったの？",
             "会社を自分のものにしたかったからです。オバディアは裏でテロ組織に武器を売ってもうけていて、邪魔なトニーを消すためにテン・リングスにトニーの殺害を頼んでいました。トニーが兵器づくりをやめると言い出したことで、ますます邪魔になりました。",
             "Why did Obadiah betray Tony?",
             "He wanted the company for himself. He was secretly making money selling weapons to terrorists, and paid the Ten Rings to kill Tony. When Tony decided to stop making weapons, he became even more of an obstacle."),
            ("テン・リングスはトニーを殺す依頼を受けていたのに、なぜ生かしていたの？",
             "ラザたちは、言われたとおり殺すより、天才のトニーに強力な武器を作らせるほうが得だと考えたからです。",
             "If the Ten Rings were paid to kill Tony, why keep him alive?",
             "Raza decided it was worth more to have the genius build powerful weapons for them than to simply kill him."),
            ("コールソンは何者？",
             "アメリカの秘密組織S.H.I.E.L.D.のエージェントです。最初は長い名前の組織として何度もトニーたちに話を聞きに来て、最後にペッパーと協力します。この後、多くのMCU作品に登場する大事な人物です。",
             "Who is Coulson?",
             "An agent of the secret agency S.H.I.E.L.D. He keeps asking to talk with Tony under the agency's long name, then teams up with Pepper at the end. He goes on to play a big part in many MCU titles."),
            ("最後に出てきた眼帯の男は誰？",
             "S.H.I.E.L.D.の長官ニック・フューリーです。「アベンジャーズ計画」の話をしに来ました。ここから、ヒーローが集まる『アベンジャーズ』へ話がつながっていきます。",
             "Who is the man with the eye patch at the end?",
             "Nick Fury, director of S.H.I.E.L.D. He has come to talk about the Avengers Initiative, which leads to The Avengers."),
            ("ローディは最後に何を見ていたの？",
             "トニーの工房にある銀色のスーツ（マーク2）を見て「次はな」とつぶやきます。次の『アイアンマン2』で、ローディがこのスーツを着ることになる前ぶれです。",
             "What was Rhodey looking at?",
             "He looks at the silver Mark II suit in Tony's workshop and says \"Next time, baby.\" It hints that he wears that suit in Iron Man 2."),
        ],
        points=[
            ("インセンの言葉がトニーを変えた", "「命を無駄にするな」というインセンの最後の言葉が、トニーが武器商人からヒーローに変わるきっかけです。インセンは『アイアンマン3』でも少しだけ登場します。",
             "Yinsen's words changed Tony", "Yinsen's last words, telling Tony not to waste his life, are what turn him from an arms dealer into a hero. Yinsen briefly appears again in Iron Man 3."),
            ("「トニー・スタークにも心がある」", "ペッパーは、洞窟で作った最初の発電装置をケースに入れて「トニー・スタークにも心がある証拠」と書いて飾っていました。この装置が、最後にトニーの命を救います。",
             "\"Proof that Tony Stark has a heart\"", "Pepper had the first reactor from the cave framed with the words \"Proof that Tony Stark has a heart.\" That same reactor saves Tony's life at the end."),
            ("ハッピーを演じているのは監督", "運転手のハッピー・ホーガンを演じるジョン・ファヴローは、この映画の監督です。ハッピーはこの後もMCUに長く登場します。",
             "Happy is played by the director", "Jon Favreau, who plays driver Happy Hogan, also directed the film. Happy appears in the MCU for years afterward."),
            ("スタン・リーのカメオ出演", "マーベル・コミックの生みの親スタン・リーが、パーティーの客として登場します。トニーに別の有名人と間違えて呼ばれるのが小ネタです。",
             "Stan Lee's cameo", "Marvel Comics legend Stan Lee appears as a guest at a party, where Tony mistakes him for a different celebrity."),
            ("ローディ役は次の作品から交代", "ローディはこの作品ではテレンス・ハワードが演じていますが、『アイアンマン2』からはドン・チードルに交代します。顔が違っても同じ人物です。",
             "Rhodey is recast", "Terrence Howard plays Rhodey here, but Don Cheadle takes over from Iron Man 2. Different face, same character."),
        ],
        next=[
            ("iron-man-2", "トニーの続きの物語。正体を明かした後のトニーと、ローディの新しいスーツ。", "Tony's story continues after revealing his identity, and Rhodey gets a suit."),
            ("avengers", "フューリーの「アベンジャーズ計画」が実現する作品。", "Fury's Avengers Initiative comes together."),
            ("iron-man-3", "アイアンマン3部作の完結編。インセンも少しだけ登場。", "The end of the Iron Man trilogy, with a brief return for Yinsen."),
        ],
        shop=[("アイアンマン Blu-ray", "アイアンマン Blu-ray", "Iron Man Blu-ray"), ("アイアンマンのフィギュア", "アイアンマン フィギュア", "Iron Man figures"),
              ("アーク・リアクターのグッズ", "アークリアクター", "Arc reactor replicas"), ("アイアンマンのレゴ", "レゴ アイアンマン", "LEGO Iron Man")],
    ),
}
