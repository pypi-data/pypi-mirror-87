from hangul.tokenizer import WordSegmenter

wsg = WordSegmenter()
aPassage = "어휴쟤가 왜저래? 정말우스워죽겠네"  # 문자열을 함수 inputAsString의
wsg.inputAsString (aPassage)                    # 매개변인으로 주거나
# inFile = "tobesegmented"        # 파일 안에 담긴 글을 낱말분할할 때에는 
# wsg.infile(inFile)              # 그 파일 이름을 함수 infile에 넘긴다.
# wsg.outfile("output.txt")
wsg.doSegment() 
# infile()이 사용되면 낱말 분할 된 글이 적힌 파일이 생겨 난다.
# 이 파일은 함수 outfile()로 지정될 수 있고 디폴트 값은 "segmented_yyddd_hhmm.txt"이다.
# with open("segmented_yyddd_hhmm.txt", "r") as f:
#   lines = f.readlines()
# for aLine in lines:
#   print(aLine)
# inputAsString()이 사용된 경우에는
print(wsg.segmentedOutput)
