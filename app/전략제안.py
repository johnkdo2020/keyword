#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 전략제안
for i in TotalData.index : 
    
    # PC
    
    # 저렴한 비용으로 상위노출과 클릭을 만들 수 있는 키워드
    if (TotalData.loc[i, "PC_Bid"] < LowBid) and (TotalData.loc[i, "PC_Clicks"] > 0) and (TotalData.loc[i, "PC_Position"] >= 3) : 
        TotalData.loc[i, "PC_Reco"] = "(1순위) 고효율 키워드 - 저비용 유효유입 키워드로 키워드 선점 필요"
        TotalData.loc[i, "Score"] = 1
        
    # 블루오션   : 매력도가 높고 // 단가는 평균 보다 낮은데 경쟁사가 상위 노출하지 않고 있는 키워드
    elif (TotalData.loc[i, "Rank"] <= 3) and (TotalData.loc[i, "PC_Bid"] <= TotalData["PC_Bid"].mean()) and (TotalData.loc[i, "temp"] <= AvgPosition) : 
        TotalData.loc[i, "PC_Reco"] = "(2순위) 블루오션 키워드 - 키워드 선점 시급"
        TotalData.loc[i, "Score"] = 2
        
    # 핵심전장   : 매력도가 높고 // 단가는 평균 보다 낮은데 경쟁사가 상위 노출 중인 키워드
    elif (TotalData.loc[i, "Rank"] <= 3) and (TotalData.loc[i, "PC_Bid"] <= TotalData["PC_Bid"].mean()) and (TotalData.loc[i, "temp"] > AvgPosition) : 
        TotalData.loc[i, "PC_Reco"] = "(3순위) 매인키워드 - 경쟁사 대비 상위노출"
        TotalData.loc[i, "Score"] = 3
        
    # 레드오션   : 매력도가 높고 // 단가가 평균 보다 높고, 경쟁사가 상위 노출 중인 키워드
    elif (TotalData.loc[i, "Rank"] <= 3) and (TotalData.loc[i, "PC_Bid"] > TotalData["PC_Bid"].mean()) and (TotalData.loc[i, "temp"] > AvgPosition) : 
        TotalData.loc[i, "PC_Reco"] = "(4순위) 레드오션 키워드 - 경쟁이 과열된 키워드로 필요에 따라 진입"
        TotalData.loc[i, "Score"] = 4
        
    # 퀘스천마크 : 매력도가 높고 // 단가가 평균 보다 높은데, 경쟁사가 상위 노출하지 않고 있는 키워드
    elif (TotalData.loc[i, "Rank"] <= 3) and (TotalData.loc[i, "PC_Bid"] > TotalData["PC_Bid"].mean()) and (TotalData.loc[i, "temp"] <= AvgPosition) : 
        TotalData.loc[i, "PC_Reco"] = "(5순위) 퀘스천마크 키워드 - 투입 대비 효율 미지수로 필요에 따라 진입"
        TotalData.loc[i, "Score"] = 5
        
    else : 
        TotalData.loc[i, "PC_Reco"] = ""
        TotalData.loc[i, "Score"] = 10
    
    # 모바일
    
    # 저렴한 비용으로 상위노출과 클릭을 만들 수 있는 키워드
    if (TotalData.loc[i, "MOBILE_Bid"] < LowBid) and (TotalData.loc[i, "MOBILE_Clicks"] > 0) and (TotalData.loc[i, "MOBILE_Position"] >= 3) : 
        TotalData.loc[i, "MOBILE_Reco"] = "(1순위) 고효율 키워드 - 저비용 유효유입 키워드로 키워드 선점 필요"
        TotalData.loc[i, "Score"] += 1
        
    # 블루오션   : 매력도가 높고 // 단가는 평균 보다 낮은데 경쟁사가 상위 노출하지 않고 있는 키워드
    elif (TotalData.loc[i, "Rank"] <= 3) and (TotalData.loc[i, "MOBILE_Bid"] <= TotalData["MOBILE_Bid"].mean()) and (TotalData.loc[i, "temp"] <= AvgPosition) : 
        TotalData.loc[i, "MOBILE_Reco"] = "(2순위) 블루오션 키워드 - 키워드 선점 시급"
        TotalData.loc[i, "Score"] += 2
        
    # 핵심전장   : 매력도가 높고 // 단가는 평균 보다 낮은데 경쟁사가 상위 노출 중인 키워드
    elif (TotalData.loc[i, "Rank"] <= 3) and (TotalData.loc[i, "MOBILE_Bid"] <= TotalData["MOBILE_Bid"].mean()) and (TotalData.loc[i, "temp"] > AvgPosition) : 
        TotalData.loc[i, "MOBILE_Reco"] = "(3순위) 매인키워드 - 경쟁사 대비 상위노출"
        TotalData.loc[i, "Score"] += 3
        
    # 레드오션   : 매력도가 높고 // 단가가 평균 보다 높고, 경쟁사가 상위 노출 중인 키워드
    elif (TotalData.loc[i, "Rank"] <= 3) and (TotalData.loc[i, "MOBILE_Bid"] > TotalData["MOBILE_Bid"].mean()) and (TotalData.loc[i, "temp"] > AvgPosition) : 
        TotalData.loc[i, "MOBILE_Reco"] = "(4순위) 레드오션 키워드 - 경쟁이 과열된 키워드로 필요에 따라 진입"
        TotalData.loc[i, "Score"] += 4
        
    # 퀘스천마크 : 매력도가 높고 // 단가가 평균 보다 높은데, 경쟁사가 상위 노출하지 않고 있는 키워드
    elif (TotalData.loc[i, "Rank"] <= 3) and (TotalData.loc[i, "MOBILE_Bid"] > TotalData["MOBILE_Bid"].mean()) and (TotalData.loc[i, "temp"] <= AvgPosition) : 
        TotalData.loc[i, "MOBILE_Reco"] = "(5순위) 퀘스천마크 키워드 - 투입 대비 효율 미지수로 필요에 따라 진입"
        TotalData.loc[i, "Score"] += 5
        
    else : 
        TotalData.loc[i, "MOBILE_Reco"] = ""
        TotalData.loc[i, "Score"] += 10

TotalData = TotalData.sort_values(by=["Reference", "Score", "monthlyQcCnt"],ascending=[True, True, False])
TotalData.reset_index(inplace=True, drop=True) 

TotalData.to_csv('./ResultData.csv', encoding = 'utf-8-sig')

TotalData

