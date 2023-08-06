import rematch as re
import rematchlib as rem
'''
regex = ".*!x{a+}.*"
document = "aaaaaa"

rgx = re.RegEx(regex)
it = rgx.findIter(document)

# for match in it:
#   print('\t'.join('!{}: {}'.format(v, match.span(v)) for v in match.variables())

count = 0

while it.hasNext():
  match = it.next()
  print('\t'.join('!{}: {}'.format(v, match.span(v)) for v in match.variables()))
  count += 1

print(count)
'''

regex = ".*!x{one} !y{two} !z{three}.*"
doc = "one two three four five ..."

rgx = re.RegEx(regex)
it = rgx.findIter(doc)
if it.hasNext():
  match = it.next()
  print(match.span("x"))

rgx = rem.compile(regex)
m = rgx.findall("dasojdos")
m = rgx.findall(doc)
m = rgx.findall(doc)
# m = rgx.finditer(doc)
print(m)
for match in m:
  print(match.groupdict())

pattern = rem.compile('.*!x{a...s}.*')
match = pattern.match("abyssal")
print(match.group("x"))