from django.shortcuts import render, redirect
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
plt.rc('font',family = 'malgun gothic')
from mysurvey.models import Survey


def surveyMain(request):
    return render(request, 'main.html')

def surveyView(request):
    return render(request, 'survey.html')

def surveyProcess(request):
    insertData(request)
    return redirect("/coffee/surveyshow") # 추가 후 분석결과 보기
    

def surveyAnalysis(request):
    rdata = list(Survey.objects.all().values())
    # print(rdata)
    df = pd.DataFrame(rdata)
    df.dropna()
    # print(df)
    
    ctab = pd.crosstab(index=df['gender'], columns=df['co_survey'])
    # print(ctab)
    
    # 카이스퀘어 추정 및 검정
    chi, pv, _, _ = stats.chi2_contingency(observed=ctab)
    print('chi:{}, pv:{}'.format(chi, pv))
    
    if pv > 0.05:
        result = "p값(유의확률)이 {} > 0.05(유의수준) 이므로 <br> 성별과 커피브랜드의 선호도는 관계가 없다.<br> <b>귀무가설을 채택</b>".format(pv)
    else:
        result = "p값(유의확률)이 {} <= 0.05(유의수준) 이므로 <br> 성별과 커피브랜드의 선호도는 관계가 있다.<br> <strong>대립가설 채택</strong>".format(pv)
    count = len(df)
    
    
    # 시각화 : 커피브랜드별 선호 건수에 대한 차트(세로막대)를 출력하시오 
    fig = plt.gcf()
    coffee_group = df.groupby(['co_survey'])['rnum'].count()
    coffee_group.plot.bar(subplots=True, color=['red','pink','yellow','orange','blue','green','skyblue'], width=0.5, rot=0)
    plt.xlabel('커피 브랜드명')
    plt.title('커피 브랜드 선호 건수')
    plt.grid()
    fig.savefig('django13coffee_chi2/mysurvey/static/images/coffee.png')
    
    return render(request, 'list.html', {'ctab':ctab.to_html(), 'result':result, 'count':count})
    
    
# --------------------
def insertData(request):  # 설문조사 결과를 db에 저장
    # print(request.POST.get('gender'), '', request.POST.get('age'), '', request.POST.get('co_survey'))- 확인용
    if request.method == 'POST':
        Survey(
            gender = request.POST.get('gender'),
            age = request.POST.get('age'),
            co_survey = request.POST.get('co_survey')
        ).save()




