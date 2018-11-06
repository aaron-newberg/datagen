import random, string, datetime

types = {
    0  : "anyURI",
    1  : "base64Binary",
    2  : "boolean",
    3  : "byte",
    4  : "date",
    5  : "dateTime",
    6  : "dayTimeDuration",
    7  : "decimal",
    8  : "double",
    9  : "duration",
    10 : "float",
    11 : "gDay",
    12 : "gMonth",
    13 : "gMonthDay",
    14 : "gYear",
    15 : "gYearMonth",
    16 : "hexBinary",
    17 : "int",
    18 : "integer",
    19 : "long",
    20 : "negativeInteger",
    21 : "nonNegativeInteger",
    22 : "nonPositiveInteger",
    23 : "positiveInteger",
    24 : "short",
    25 : "string",
    26 : "time",
    27 : "unsignedByte",
    28 : "unsignedInt",
    29 : "unsignedLong",
    30 : "unsignedShort",
    31 : "yearMonthDuration"#,
    # 32 : "point",
    # 33 : "longLatPoint",
    # 34 : "IRI"
}

def stringgenWrapper():
    return stringgen(100, True, True)

def stringgen(length, numbers, specialChars):
    chars = string.ascii_letters 
    if numbers == True:
        chars = chars + string.digits
    if specialChars == True:
        chars = chars + '~!@#$%^*()_+[]\,./;<>?|| '
    return ''.join(random.choice(chars) for i in range(random.randint(1,length)))

def anyURIgen():
    return stringgen(25, True, False)

def base64Binarygen():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(1, 5) * 4))

def booleangen():
    return "true" if random.randint(0, 1) == 0 else "false"

def bytegen():
    return random.randint(-127, 128)

def dategen():
    thirtyOneDays = [1, 3, 5, 7, 8, 10, 12]
    year = random.randint(1970, datetime.datetime.now().year)
    month = random.randint(1, 12)
    if month == 2:
        day = random.randint(1, 28)
    elif month in thirtyOneDays:
        day = random.randint(1, 31)
    else:
        day = random.randint(1, 30)
    return str(year) + '-' + str('{:02d}'.format(month)) + '-' + str('{:02d}'.format(day))

def dateTimegen():
    return dategen() + 'T' + timegen()

def dayTimeDurationgen():
    return ("-" if random.randint(0, 100) < 70 else "") + "P" + str(random.randint(0, 9999)) + "DT" + str(random.randint(0, 9999)) + "H" 

def decimalgen():
    return '{:f}'.format(random.uniform(-9999999999, 9999999999))

def doublegen():
    return decimalgen()

def durationgen():
    years = random.randint(0, 15)
    months = random.randint(0, 15)
    days = random.randint(0, 15)
    hours = random.randint(0, 15)
    minutes = random.randint(0, 15)
    seconds = random.randint(0, 15)
    return "P" + ((str(years) + "Y") if years > 0 else "") + \
                 ((str(months) + "M") if months > 0 else "") + \
                 ((str(days) + "D") if months > 0 else "") + \
                 ("T" if hours > 0 or minutes > 0 or seconds > 0 else "") + \
                 ((str(hours) + "H") if hours > 0 else "") + \
                 ((str(minutes) + "M") if minutes > 0 else "") + \
                 ((str(seconds) + "S") if seconds > 0 else "")

def floatgen():
    return '{:f}'.format(random.uniform(-9999, 9999))

def gDaygen():
    return "---" + '{:02d}'.format(random.randint(1, 31))

def gMonthgen():
    return "--" + '{:02d}'.format(random.randint(1, 12))

def gMonthDaygen():
    month = random.randint(1, 12)
    thirtyOneDays = [1, 3, 5, 7, 8, 10, 12]
    if month == 2:
        day = random.randint(1,28)
    elif month in thirtyOneDays:
        day = random.randint(1, 31) 
    else:
        day = random.randint(1, 30)
    return "--" '{:02d}'.format(month) + '-{:02d}'.format(day)

def gYeargen():
    return str(random.randint(1970, datetime.datetime.now().year))

def gYearMonthgen():
    return gYeargen() + '-{:02d}'.format(random.randint(1, 12))

def hexBinarygen():
    chars = string.hexdigits
    return ''.join(random.choice(chars) for i in range(random.randint(1, 13) * 2))

def intgen():
    return random.randint(-2147483648, 2147483647)

def integergen():
    return random.randint(-18446744073709551615, 18446744073709551615)

def longgen():
    return random.randint(-9223372036854775808, 9223372036854775807)

def negativeIntegergen():
    return random.randint(-18446744073709551615, -1)

def nonNegativeIntegergen():
    return random.randint(0, 18446744073709551615)

def nonPositiveIntegergen():
    return random.randint(-18446744073709551615, 0)

def positiveIntegergen():
    return random.randint(1, 18446744073709551615)

def shortgen():
    return random.randint(-32768, 32767)

def timegen():
    return str('{:02d}'.format(random.randint(0,23))) + ':' + str('{:02d}'.format(random.randint(0,59))) + ':' + str('{:02d}'.format(random.randint(0,59)))

def unsignedBytegen():
    return random.randint(0, 255)

def unsignedIntgen():
    return random.randint(0, 4294967295)

def unsignedLonggen():
    return random.randint(0, 18446744073709551615)

def unsignedShortgen():
    return random.randint(0, 65535)

def yearMonthDurationgen():
    return ("-" if random.randint(0, 100) > 70 else "") + "P" + str(random.randint(0, 999)) + "Y" + str(random.randint(0,999)) + "M"

def pointgen():
    return

def longLatPointgen():
    return

def IRIgen():
    return

def getTypeSize():
    return len(types)

def getType(index):
    return types[index]

def runGenFunction(index):
    return funs[index]()

funs = {
    0  : anyURIgen,
    1  : base64Binarygen,
    2  : booleangen,
    3  : bytegen,
    4  : dategen,
    5  : dateTimegen,
    6  : dayTimeDurationgen,
    7  : decimalgen,
    8  : doublegen,
    9  : durationgen,
    10 : floatgen,
    11 : gDaygen,
    12 : gMonthgen,
    13 : gMonthDaygen,
    14 : gYeargen,
    15 : gYearMonthgen,
    16 : hexBinarygen,
    17 : intgen,
    18 : integergen,
    19 : longgen,
    20 : negativeIntegergen,
    21 : nonNegativeIntegergen,
    22 : nonPositiveIntegergen,
    23 : positiveIntegergen,
    24 : shortgen,
    25 : stringgenWrapper,
    26 : timegen,
    27 : unsignedBytegen,
    28 : unsignedIntgen,
    29 : unsignedLonggen,
    30 : unsignedShortgen,
    31 : yearMonthDurationgen#,
    # 32 : pointgen,
    # 33 : longLatPointgen,
    # 34 : IRIgen
}