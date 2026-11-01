# 作品別キャラクター相関図のデータ。作品を足すときは RELATION_MAPS に1件追加して `python3 src/build.py` を実行する。
#
# 作品のキー: titles_*.py の slug と同じにする（視聴順ガイドから自動でリンクされる）
# people（人物）:
#   id:     半角英数字（images の キーと同じ）
#   role:   "lead"（中心の2人・いちばん大きい）/ "main"（主要人物）/ "sub"（脇役・小さめ）
#   side:   "hero"（主人公側）/ "neutral"（どちらでもない）/ "villain"（敵側）… アイコンの縁の色になる
#   x, y:   相関図の中の位置（中心が 0,0。右が +x、下が +y。1目盛り＝約1px）。
#           省略すると ring（1=内側, 2=外側）と angle（度。0=右、90=下）から自動で置く。
#           ring も省略すると、空いている角度に自動で並べる。
#   name / name_en, actor / actor_en, group / group_en, desc / desc_en
# links（関係の線）:
#   a, b:   人物の id
#   type:   "love"（恋愛）/ "family"（家族）/ "friend"（友情・親友）/ "ally"（協力）/ "enemy"（敵対）/ "org"（組織上の関係）
#   label / label_en: 線の近くに出す短い言葉（"\n" で改行）
#   bend:   線を曲げる量（-1〜1。省略でまっすぐ）、at: ラベルの位置（0〜1。省略で 0.5）
#
# 顔写真は IMAGES に登録する。利用許諾が確認できた画像だけを src/chars/ に置き、出典とライセンスを必ず書く。
# 登録がない人物は、イニシャルの仮アイコンで表示される（後から IMAGES に足すだけで差し替わる）。

LINK_TYPES = {
    "love": ("恋愛", "Romance"),
    "family": ("家族", "Family"),
    "friend": ("友情・親友", "Friendship"),
    "ally": ("協力", "Allies"),
    "enemy": ("敵対", "Enemies"),
    "org": ("組織・仕事", "Organization"),
}

RELATION_MAPS = {
    "iron-man": dict(
        updated="2026-11-01",
        lead="トニー・スタークとペッパー・ポッツを中心に、『アイアンマン』（2008年）に登場する人物の関係をまとめました。上が仲間、下が敵です。",
        lead_en="Who's who in Iron Man (2008), with Tony Stark and Pepper Potts at the center. Friends are above, enemies below.",
        groups=[
            dict(x=-200, y=-580, label="トニーの仲間", label_en="Tony's circle"),
            dict(x=300, y=-650, label="S.H.I.E.L.D.", label_en="S.H.I.E.L.D."),
            dict(x=230, y=780, label="スターク・インダストリーズ", label_en="Stark Industries"),
            dict(x=-250, y=860, label="テン・リングス（テロ組織）", label_en="The Ten Rings"),
        ],
        people=[
            dict(id="tony", role="lead", side="hero", x=-145, y=0,
                 name="トニー・スターク", name_en="Tony Stark", actor="ロバート・ダウニー・Jr.", actor_en="Robert Downey Jr.",
                 group="主人公", group_en="Hero",
                 desc="天才発明家で、兵器会社スターク・インダストリーズの社長。アフガニスタンで誘拐され、洞窟でパワードスーツを作って脱出する。自分の会社の兵器が悪用されていると知り、アイアンマンとして戦い始める。最後に「私がアイアンマンだ」と正体を公表する。",
                 desc_en="A genius inventor and CEO of the weapons maker Stark Industries. Kidnapped in Afghanistan, he builds a suit of armor in a cave to escape. When he learns his company's weapons are being misused, he starts fighting as Iron Man, and ends by announcing \"I am Iron Man.\""),
            dict(id="pepper", role="lead", side="hero", x=145, y=0,
                 name="ペッパー・ポッツ", name_en="Pepper Potts", actor="グウィネス・パルトロー", actor_en="Gwyneth Paltrow",
                 group="トニーの秘書", group_en="Tony's assistant",
                 desc="トニーの有能な秘書。わがままなトニーを支え、お互いに惹かれ合っている。トニーに頼まれて会社のデータを調べ、オバディアの裏切りを突き止める。",
                 desc_en="Tony's capable assistant. She keeps him on track and the two are drawn to each other. At Tony's request she searches the company files and uncovers Obadiah's betrayal."),
            dict(id="rhodey", role="main", side="hero", x=-370, y=-200,
                 name="ジェームズ・ローズ（ローディ）", name_en="James \"Rhodey\" Rhodes", actor="テレンス・ハワード", actor_en="Terrence Howard",
                 group="トニーの親友", group_en="Tony's best friend",
                 desc="アメリカ空軍の中佐で、軍とスターク社の連絡係。トニーの親友で、行方不明になったトニーを探し続けた。次作『アイアンマン2』からはドン・チードルが演じる。",
                 desc_en="A U.S. Air Force lieutenant colonel and the military's liaison to Stark Industries. Tony's best friend, he kept searching when Tony went missing. Don Cheadle takes over the role from Iron Man 2."),
            dict(id="jarvis", role="main", side="hero", x=-110, y=-330,
                 name="J.A.R.V.I.S.（ジャーヴィス）", name_en="J.A.R.V.I.S.", actor="ポール・ベタニー（声）", actor_en="Paul Bettany (voice)",
                 group="トニーのAI", group_en="Tony's AI",
                 desc="トニーが作った人工知能。家の管理からスーツの操作まで手伝う執事のような存在。のちに『エイジ・オブ・ウルトロン』でヴィジョンにつながる。",
                 desc_en="The artificial intelligence Tony built. It runs his house and helps operate the suit, like a butler. It later leads to Vision in Age of Ultron."),
            dict(id="happy", role="sub", side="hero", x=90, y=-370,
                 name="ハッピー・ホーガン", name_en="Happy Hogan", actor="ジョン・ファヴロー", actor_en="Jon Favreau",
                 group="運転手・ボディガード", group_en="Driver and bodyguard",
                 desc="トニーの運転手兼ボディガード。演じるジョン・ファヴローはこの映画の監督でもある。のちの作品ではピーター・パーカーの世話役にもなる。",
                 desc_en="Tony's driver and bodyguard, played by the film's director Jon Favreau. In later films he also looks after Peter Parker."),
            dict(id="dummy", role="sub", side="hero", x=-300, y=-430,
                 name="ダミー", name_en="Dum-E", actor="（ロボットアーム）", actor_en="(robot arm)",
                 group="工房のロボット", group_en="Workshop robot",
                 desc="トニーの工房で働くロボットアーム。失敗ばかりで叱られるが、最後にはトニーの命を救う。",
                 desc_en="A robot arm in Tony's workshop. It keeps getting scolded for mistakes, but saves Tony's life at the end."),
            dict(id="yinsen", role="main", side="hero", x=-370, y=190,
                 name="ホー・インセン", name_en="Ho Yinsen", actor="ショーン・トーブ", actor_en="Shaun Toub",
                 group="洞窟で出会った医師", group_en="Doctor in the cave",
                 desc="トニーと一緒にテン・リングスに捕まっていた医師。トニーの胸に電磁石を付けて命を救い、スーツ作りを手伝う。脱出のときに自分を犠牲にし、「命を無駄にするな」とトニーに言い残す。",
                 desc_en="A doctor held captive with Tony by the Ten Rings. He saves Tony's life with an electromagnet in his chest and helps build the suit. He sacrifices himself during the escape and tells Tony not to waste his life."),
            dict(id="coulson", role="main", side="neutral", x=330, y=-260,
                 name="フィル・コールソン", name_en="Phil Coulson", actor="クラーク・グレッグ", actor_en="Clark Gregg",
                 group="S.H.I.E.L.D.", group_en="S.H.I.E.L.D.",
                 desc="「戦略国土調停補強配備局」という長い名前の組織のエージェント。のちにS.H.I.E.L.D.と名乗る。最後はペッパーと協力してオバディアを止める。この後もMCUのあちこちに登場する。",
                 desc_en="An agent of the Strategic Homeland Intervention, Enforcement and Logistics Division, later called S.H.I.E.L.D. He helps Pepper stop Obadiah, and goes on to appear across the MCU."),
            dict(id="fury", role="sub", side="neutral", x=300, y=-510,
                 name="ニック・フューリー", name_en="Nick Fury", actor="サミュエル・L・ジャクソン", actor_en="Samuel L. Jackson",
                 group="S.H.I.E.L.D.長官", group_en="Director of S.H.I.E.L.D.",
                 desc="エンドクレジットの後にだけ登場するS.H.I.E.L.D.の長官。トニーに「アベンジャーズ計画」の話をしに来る。ここからアベンジャーズの物語が始まる。",
                 desc_en="The director of S.H.I.E.L.D., seen only after the end credits. He visits Tony to talk about the Avengers Initiative, which starts the road to The Avengers."),
            dict(id="christine", role="sub", side="neutral", x=360, y=250,
                 name="クリスティン・エヴァハート", name_en="Christine Everhart", actor="レスリー・ビブ", actor_en="Leslie Bibb",
                 group="雑誌記者", group_en="Reporter",
                 desc="『ヴァニティ・フェア』の記者。トニーの兵器ビジネスを批判し、のちにスターク社の兵器がテロ組織に渡っていることをトニーに伝える。",
                 desc_en="A Vanity Fair reporter who criticizes Tony's weapons business, and later shows him that Stark weapons have reached a terrorist group."),
            dict(id="obadiah", role="main", side="villain", x=190, y=440,
                 name="オバディア・ステイン", name_en="Obadiah Stane", actor="ジェフ・ブリッジス", actor_en="Jeff Bridges",
                 group="スターク社の重役", group_en="Stark Industries executive",
                 desc="トニーの父ハワードの共同経営者で、トニーの父親代わり。実は裏でテロ組織に兵器を売り、トニーの誘拐も仕組んでいた。最後は巨大なスーツ「アイアンモンガー」でトニーと戦う。",
                 desc_en="Howard Stark's business partner and a father figure to Tony. Secretly he sells weapons to terrorists and arranged Tony's kidnapping. He fights Tony in the giant Iron Monger suit."),
            dict(id="howard", role="sub", side="hero", x=-30, y=300,
                 name="ハワード・スターク", name_en="Howard Stark", actor="（写真などで登場）", actor_en="(seen in photos)",
                 group="トニーの父（故人）", group_en="Tony's late father",
                 desc="スターク・インダストリーズの創業者で、トニーの父。この映画ではすでに亡くなっていて、写真などで登場する。若いころの姿は『キャプテン・アメリカ／ザ・ファースト・アベンジャー』で描かれる。",
                 desc_en="Founder of Stark Industries and Tony's father. He has died before this film and appears in photos. His younger self appears in Captain America: The First Avenger."),
            dict(id="riva", role="sub", side="villain", x=320, y=630,
                 name="ウィリアム・ギンター・リヴァ", name_en="William Ginter Riva", actor="ピーター・ビリングスリー", actor_en="Peter Billingsley",
                 group="スターク社の科学者", group_en="Stark Industries scientist",
                 desc="オバディアの下でスーツを作らされる科学者。トニーが洞窟で作った小型の動力源を再現できず、オバディアに怒鳴られる。",
                 desc_en="A scientist forced to build a suit for Obadiah. He can't recreate the small power source Tony built in a cave, and Obadiah yells at him."),
            dict(id="raza", role="main", side="villain", x=-260, y=510,
                 name="ラザ", name_en="Raza", actor="ファラン・タヒール", actor_en="Faran Tahir",
                 group="テン・リングスのリーダー", group_en="Ten Rings leader",
                 desc="テロ組織テン・リングスのリーダー。トニーを誘拐し、兵器を作らせようとする。裏でオバディアと取引していたが、最後は裏切られる。",
                 desc_en="Leader of the terrorist group the Ten Rings. He kidnaps Tony to force him to build weapons. He has a secret deal with Obadiah, who betrays him in the end."),
            dict(id="abu", role="sub", side="villain", x=-330, y=720,
                 name="アブ・バカール", name_en="Abu Bakaar", actor="サイード・バドレヤ", actor_en="Sayed Badreya",
                 group="テン・リングスの幹部", group_en="Ten Rings lieutenant",
                 desc="ラザの部下。洞窟でトニーとインセンを見張る。",
                 desc_en="Raza's lieutenant who guards Tony and Yinsen in the cave."),
        ],
        links=[
            dict(a="tony", b="pepper", type="love", label="秘書\n惹かれ合う", label_en="Assistant,\nmutual feelings"),
            dict(a="tony", b="rhodey", type="friend", label="親友", label_en="Best friend"),
            dict(a="tony", b="jarvis", type="ally", label="AI執事", label_en="AI butler"),
            dict(a="tony", b="dummy", type="ally", label="工房の助手", label_en="Lab helper", at=0.62),
            dict(a="tony", b="happy", type="org", label="運転手", label_en="Driver", at=0.6),
            dict(a="tony", b="yinsen", type="friend", label="命の恩人", label_en="Saved his life"),
            dict(a="tony", b="howard", type="family", label="父", label_en="Father", at=0.55),
            dict(a="tony", b="coulson", type="org", label="S.H.I.E.L.D.の窓口", label_en="S.H.I.E.L.D. contact", at=0.6),
            dict(a="tony", b="fury", type="org", label="アベンジャーズ計画", label_en="Avengers Initiative", at=0.72),
            dict(a="tony", b="christine", type="love", label="一夜の相手\n（記者）", label_en="One-night fling\n(reporter)", at=0.62, bend=0.3),
            dict(a="tony", b="obadiah", type="enemy", label="父親代わり→黒幕", label_en="Mentor → betrayer", at=0.58),
            dict(a="tony", b="raza", type="enemy", label="誘拐した", label_en="Kidnapped him", at=0.55),
            dict(a="pepper", b="obadiah", type="enemy", label="裏切りを暴く", label_en="Exposes him", at=0.45),
            dict(a="pepper", b="coulson", type="ally", label="協力して\nステインを止める", label_en="Team up to\nstop Stane", at=0.5),
            dict(a="coulson", b="fury", type="org", label="上司", label_en="Boss"),
            dict(a="howard", b="obadiah", type="org", label="共同経営者", label_en="Business partner"),
            dict(a="obadiah", b="riva", type="org", label="部下", label_en="Employee"),
            dict(a="obadiah", b="raza", type="enemy", label="裏取引→裏切り", label_en="Secret deal → betrayal", at=0.5),
            dict(a="raza", b="yinsen", type="enemy", label="捕虜にした", label_en="Holds captive"),
            dict(a="raza", b="abu", type="org", label="部下", label_en="Lieutenant"),
        ],
    ),
}

# 顔写真（人物の id → 画像の情報）。利用許諾を確認した画像だけを登録する。
# file は src/chars/ の中のファイル名。ビルドで assets/chars/ にコピーされる。
# 例: "tony": dict(file="robert-downey-jr.jpg", author="撮影者名", license="CC BY-SA 4.0",
#                  license_url="https://creativecommons.org/licenses/by-sa/4.0/", source_url="https://commons.wikimedia.org/wiki/File:...")
IMAGES = {}
