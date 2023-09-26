anpr = [
    {"estimate1.jpg": "HO86M"},
    {"estimate2.jpeg": "BS826N"},
    {"estimate3.jpeg": "KBO96"},
    None,
    None,
    None,
    None,
    {"vehicle10.jpeg": "KCA650X"},
    {"vehicle11.jpeg": "KBS826N"},
    {"vehicle2.jpg": "IMARIGA17"},
    {"vehicle3.jpg": "KCX6235S"},
    {"vehicle4.jpg": "108CCM"},
    {"vehicle5.jpeg": "KBP550A"},
    {"vehicle6.jpeg": "KBF685A"},
    {"vehicle7.jpeg": "KBG916V"},
    {"vehicle8.jpeg": "KAZ179X"},
    {"vehicle9.jpeg": "KAN801Y"},
]

for item in anpr:
    if item != None:
        for k, v in item.items():
            print(v)

    # for k, v in i:
    #     print(k)
