from jamo import h2j, j2hcj

sample_text = "서버이용자분들께말씀드립니다저는이곳에서무언가를하고있습니다"
prit = j2hcj(h2j(sample_text))

print(prit)
