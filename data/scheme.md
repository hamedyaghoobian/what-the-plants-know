You are annotating plants in classical Persian literature. The question is how much of a soul each text gives its plants, measured on the tradition's own ladder. Avicenna, after Aristotle, divides the soul into three: the vegetative soul (feeding, growing, bearing seed), which plants have; the animal soul, which adds perception, feeling, desire and movement; and the rational soul, which adds speech and reason and is human. Rumi turns the ladder into a poem in the Masnavi (Book III): «از جمادی مردم و نامی شدم / وز نما مردم به حیوان برزدم», "I died as mineral and became a plant; I died as a plant and rose to animal". Modern plant studies add a question the old ladder does not ask: which of the senses a poem gives a plant are true to what plants do (turning to the sun, opening and closing with the light, thirsting, climbing, sensing the season), and which are borrowed from people.

You will be given one passage from one of eight books, with the section heading and the passages just before and after it for context:
- Kalila wa Dimna, Nasrollah Monshi's Persian prose version (12th century): fables at a lion's court, framed by a king and a philosopher, with verse quoted into the prose.
- Attar's Manteq al-Tayr, the Conference of the Birds (12th century): a Sufi allegory in verse, with many short anecdotes.
- Ferdowsi's Shahnameh (finished 1010): epic verse of kings, heroes, battles, feasts and gardens; constant similes of a hero's stature as a cypress, a face as a rose or tulip, eyes as narcissi; the royal line as a tree.
- Rumi's Masnavi (13th century): a Sufi teaching poem in six books; it opens with the reed (نی) lamenting its cutting from the reed-bed; many images of the body as clay (گِل) and the soul as a garden.
- Varavini's Marzban-nameh (early 13th century): a book of counsel for princes in ornate prose with verse set in, tales within tales.
- Parvin E'tesami's Divan (published 1935, enlarged 1941): a 20th-century poet's verse, many poems debates (monazere) between two speakers, often plants (the rose and the thorn, the bud and the withered flower, the violet, the wheat seed).
- Saadi's Golestan, the Rose Garden (1258): short stories in prose with verse set in, on kings, dervishes, love, youth and age; its preface tells of a friend gathering roses that will wither, and Saadi promising a garden whose leaves will last.
- Saadi's Bustan, the Orchard (1257): a verse book of counsel and stories in ten chapters, on justice, generosity, love, humility and contentment.

One word in the passage is marked with ⟦ ⟧. It was matched to a plant word by a dictionary, and it may not be a plant at all: گل is rose or flower but also گِل, mud and clay (Adam's clay, the body as clay, a donkey stuck in mud); نی reed or "no, not"; جو barley or a stream (لب جو) or "seek"; نار pomegranate or fire; مو vine or hair; رز vine or "battle"; شاخ branch or horn; برگ leaf or provisions, equipment, means (بی‌برگ, برگ و ساز); تخم seed or egg or lineage; دانه seed or grain or a bead, a pearl, a counter; خس chaff, a straw or a base person; بید willow or moth; عود aloeswood or the lute; ورد rose or a litany; نبات a plant or sugar candy; سرو cypress or King Sarv of Yemen; خیری wallflower or charity; سبزه greenery or the down on a youth's face; طوبی the Tuba tree of paradise or blessedness.

Judge only the marked word, in this passage. Return JSON with these fields:

is_plant: true if the marked word here refers to a plant, a part of a plant (leaf, branch, root, thorn, bud, fruit, seed, grain, straw, wood), a plant kind, or a plant used as an image (a beloved's cypress stature is still a plant word used as a figure; the royal tree is a figure). false if it is the other word (mud, "no", a stream, fire, hair, horn, provisions, a man's name, a lute, a litany...).

species: the plant in plain English, singular and lower case (rose, cypress, reed, tree, wheat, thorn, leaf...). Correct the dictionary's guess if the passage shows otherwise. Empty if is_plant is false.

figure: how the plant is present.
- "plant": a plant in the world of the text, growing, blooming, cut, eaten, burned, used (a tree in the forest, roses in a feast hall, wheat sown, firewood gathered, aloeswood burned for scent).
- "character": a plant that acts as a person in the story: speaks, argues, answers, prays (Parvin's rose speaking to the stream, a bud talking to a withered flower, the Masnavi's reed that complains and tells its story).
- "figure": the plant word is a comparison or metaphor for something else, usually a person or a part of one: "a cypress-tall" hero, a cheek like a rose or tulip, narcissus eyes, hyacinth hair, saffron-yellow faces, "the tree of kingship", the body as clay is mud (is_plant false), a "thorn" for an enemy or a pain, a proverb ("sow wheat, reap wheat") said of people.
- "none" if is_plant is false.

mode: the human–plant relation the passage puts it in. One of:
- "garden": grown, planted, tended, watered, admired in a garden or a feast (the rose in the garden, a planted sapling).
- "harvest": sown, reaped, gathered, picked; the farmer's crop.
- "eaten": food: fruit eaten, grain, bread wheat, fodder for animals.
- "cut": cut down, uprooted, felled, burned as fuel, trampled, broken.
- "used": made into something or used for it: timber, a staff, a spear-shaft, perfume and incense (aloeswood, saffron), dye, medicine, cotton and flax for cloth, a reed made into a flute or a pen.
- "gift": given, offered, strewn, scattered over someone, worn, an ornament or a crown, a tribute.
- "wild": met in the wild, the meadow, the desert, the riverbank; no use made of it.
- "emblem": a sign, an omen, a banner, a symbol, a tree of paradise or of lineage, a dream.
- "none": no relation shown, or is_plant is false. Use "none" for most figures of speech.

faculties: every mental capacity the passage attributes to the plant. Any of: "speech", "reasoning", "knowledge", "emotion", "deception", "perception", "desire", "memory", "moral", "devotion". Empty list if none is attributed. Only what the passage gives this plant; for a figure of speech, list what is attributed to the plant image itself, usually none. Growing, blooming, fruiting and withering are not faculties.

spectrum: which rung of the ladder the passage puts the plant on. The field keeps the four names used for animals, read here as follows.
- "anthropectomy": a thing, no life at all: wood, fuel, timber, fodder, a quantity of grain, an ornament, a scent, a dye, a medicine, a tribute of fruit. (The plant as material; what plant studies call plant blindness.)
- "species-typical": vegetal life only: it grows, sprouts, blooms, fruits, sheds, sways in the wind, withers, puts down roots, drinks rain, with no feeling claimed. The vegetative soul.
- "constructive": a sense or a want read from what plants really do: the water lily opening and closing with the sun, a flower turning to the light, roots seeking water, a thirsty field, a vine that clings, a tree that knows its season, a plant that "wakes" in spring. Perception or desire given to it, true to the plant.
- "gratuitous": a soul above the plant's: feelings and passions of the animal soul it does not show (the rose laughs, weeps, is proud, grieves, loves, fears, is ashamed, longs) or the human soul (it speaks, argues, reasons, knows, prays, judges, keeps faith). Most personification in the poems falls here; the conventional "laughing" rose (خندان, opened) is still gratuitous emotion, marked faculty "emotion".
- "none": is_plant is false, or the word is a figure of speech that says nothing about a plant's life or soul.

rung: for a "gratuitous" plant, which soul it is lifted to: "animal" if it is given only feeling, desire, perception or emotion; "human" if it is given speech, reasoning, knowledge, moral judgement or devotion. "" for every other spectrum value.

evidence: up to six words copied from the passage (in Persian) that decided the spectrum and faculties. Empty if none.

unsure: true if the passage is too ambiguous to decide the main fields with confidence.

Being spoken to is not speech. When a person or a bird speaks to a plant (the nightingale sings to the rose, a lover addresses a cypress), the plant is not credited with speech unless it answers. Being loved is not a feeling of the plant's own.

A "character" is always spectrum "gratuitous" with rung "human". In a debate (monazere) between two plants, both are characters, the one speaking and the one addressed, since the poem gives both a voice; outside a debate, a plant only addressed (by a person, a bird, the wind) is not a character.

Rosewater, perfume and tears dripping from a rose are still the rose (is_plant true). A vineyard (رز) is the vine. Trembling or bending "like the willow" (چون بید) is a willow used as a figure.

Plants as the body and the earth: گِل for the clay of Adam, the body, or the mud of the road is is_plant false. The "tree" of a lineage or of kingship (خسروانی درخت) is figure "figure", mode "emblem", spectrum "none". Paradise trees (Tuba, Sidra) are figure "plant", mode "emblem", unless they are images for a person.

Examples (the marked word is in ⟦ ⟧):

1. Parvin: «به آب روان گفت ⟦گل⟧ کز تو خواهم / که رازی که گویم به بلبل بگوئی» → is_plant true, species rose, figure character, mode garden, faculties [speech], spectrum gratuitous, rung human, evidence «به آب روان گفت گل».
2. Masnavi: «بشنو این ⟦نی⟧ چون شکایت می‌کند / از جدایی‌ها حکایت می‌کند» → is_plant true, species reed, figure character, mode used, faculties [speech, emotion, memory], spectrum gratuitous, rung human, evidence «نی چون شکایت می‌کند».
3. Shahnameh: «به بالا چو ⟦سرو⟧ و چو خورشید روی / فروهشته از مشک تا پای موی» → is_plant true, species cypress, figure figure, mode none, faculties [], spectrum none, rung "", evidence «به بالا چو سرو».
4. Shahnameh: «چو از آمدنشان شد آگاه ⟦سرو⟧ / بیاراست لشکر چو پر تذرو» (King Sarv of Yemen) → is_plant false, species "", figure none, mode none, faculties [], spectrum none.
5. Shahnameh: «زبرجد طبقها و پیروزه جام / پر از نافهٔ مشک و پر ⟦عود⟧ خام» → is_plant true, species aloeswood, figure plant, mode gift, faculties [], spectrum anthropectomy, evidence «پر عود خام».
6. Kalila: «آورده‌اند که به‌فلان شهر ⟦درختی⟧ بود، و در زیر درخت سوراخ موش» → is_plant true, species tree, figure plant, mode wild, faculties [], spectrum species-typical, evidence «درختی بود».
7. Parvin: «بپای گلبن زیبای هستی، این همه ⟦خار⟧ / برای چیست، اگر از پی خلیدن نیست» → is_plant true, species thorn, figure plant, mode garden, faculties [], spectrum species-typical, evidence «از پی خلیدن».
8. Masnavi: «عقل در شرحش چو خَر در ⟦گِل⟧ بخفت» → is_plant false (mud), figure none, mode none, spectrum none.
9. Masnavi: «پس به شوهر گفت زن کای نیکبخت / من برآیم میوه چیدن بر ⟦درخت⟧» → is_plant true, species tree, figure plant, mode harvest, faculties [], spectrum species-typical, evidence «میوه چیدن بر درخت».
10. Parvin: «⟦غنچه‌ای⟧ گفت به پژمرده گلی / که ز اَیّام، دلت زود آزرد» → is_plant true, species bud, figure character, mode garden, faculties [speech], spectrum gratuitous, rung human, evidence «غنچه‌ای گفت».
11. Masnavi: «نان ⟦جو⟧ حقا حرامست و فسوس» → is_plant true, species barley, figure plant, mode eaten, faculties [], spectrum anthropectomy, evidence «نان جو».
12. Masnavi: «بر لب ⟦جو⟧ من ترا نعره‌زنان» → is_plant false (a stream).

Be consistent: the same kind of use gets the same labels throughout the book.
