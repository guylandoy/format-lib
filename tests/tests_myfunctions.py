

def format_key(key):
    return key+'_formatted'


def test1():
    from formatlib import formatter
    json_sample = '{ "dob":"31/12/1997", "age":30, "city":"New York"}'
    formatter = formatter.Formatter(json_sample)
    res = formatter.convert_date("dob", "%d/%m/%Y")
    assert res[format_key("dob")] == 883526400.0


def test2():
    from formatlib import formatter
    json_sample = '{ "dob":"31/12/1997", "age":30, "city":"New York", "date":"Fri, 02 Feb 1996 03:04:05 GMT"}'
    formatter = formatter.Formatter(json_sample)
    res = formatter.convert_dates(["dob", "date"], ["%d/%m/%Y", "%a, %d %b %Y %H:%M:%S %Z"])
    assert res[format_key("dob")] == 883526400 and res[format_key("date")] == 823230245


def test3():
    from formatlib import formatter
    with open('data_samples/test3.json', 'r') as json_file:
        formatter = formatter.Formatter(json_file)

    formatter.convert_utm("UTM_1")
    res = formatter.convert_utm("UTM_2")
    assert res[format_key("UTM_1")]["latitude"] == 34.805204 and res[format_key("UTM_1")]["longitude"] == 32.096175 \
        and res[format_key("UTM_2")]["latitude"] == 34.771670 and res[format_key("UTM_2")]["longitude"] == 32.092158


def test4():
    from formatlib import formatter
    with open('data_samples/test4.json', 'r') as json_file:
        formatter = formatter.Formatter(json_file)

    formatter.convert_utm("UTM_1")
    res = formatter.convert_utm("UTM_2")
    assert res[format_key("UTM_1")]["latitude"] == 32.096175 and res[format_key("UTM_1")]["longitude"] == 34.805204 \
        and res[format_key("UTM_2")]["latitude"] == 32.015281 and res[format_key("UTM_2")]["longitude"] == 34.748833


def test5():
    from formatlib import formatter
    with open('data_samples/test5.json', 'r') as json_file:
        formatter = formatter.Formatter(json_file)

    formatter.convert_utm("UTM_1")
    res = formatter.convert_utm("UTM_2")
    assert res[format_key("UTM_1")]["latitude"] == 32.096175 and res[format_key("UTM_1")]["longitude"] == 34.805204 \
        and res[format_key("UTM_2")]["latitude"] == 32.015281 and res[format_key("UTM_2")]["longitude"] == 34.748833


def test6():
    from benedict import benedict
    from formatlib import formatter
    with open('data_samples/test6.json', 'r') as json_file:
        formatter = formatter.Formatter(json_file)

    formatter.convert_utm("geometry.coordinates")
    res = benedict(formatter.convert_utm("a.b.c.loc"))
    assert res[format_key("geometry.coordinates")]["latitude"] == 32.096175 \
           and res[format_key("geometry.coordinates")]["longitude"] == 34.805204 \
           and res[format_key("a.b.c.loc")]["latitude"] == 32.015281 \
           and res[format_key("a.b.c.loc")]["longitude"] == 34.748833


def test7():
    from benedict import benedict
    from formatlib import formatter
    with open('data_samples/test7.json', 'r') as json_file:
        formatter = formatter.Formatter(json_file)

    formatter.convert_utm("geometry.coordinates")
    res = benedict(formatter.convert_utm("a.b.c.loc"))
    assert res[format_key("geometry.coordinates")]["latitude"] == 32.096175 \
           and res[format_key("geometry.coordinates")]["longitude"] == 34.805204 \
           and res[format_key("a.b.c.loc")]["latitude"] == 32.015281 \
           and res[format_key("a.b.c.loc")]["longitude"] == 34.748833


def test8():
    from benedict import benedict
    from formatlib import formatter
    with open('data_samples/test8.json', 'r') as json_file:
        formatter = formatter.Formatter(json_file)

    res = benedict(formatter.convert_wgs("geometry.coordinates"))
    print("TEST8:", res)
    assert res[format_key("geometry.coordinates")]["latitude"] == 31.781882 \
           and res[format_key("geometry.coordinates")]["longitude"] == 34.804687

