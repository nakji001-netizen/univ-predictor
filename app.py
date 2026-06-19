# ... existing code ...
    # 상단 요약
    st.success("✅ 변환 완료! 아래 표에서 지원 가능한 전체 대학 리스트를 확인하세요.")
    m1, m2 = st.columns(2)
    m1.metric("입력한 5등급 내신", f"{input_grade_5:.2f} 등급")
    m2.metric("최종 9등급 환산 내신", f"{converted_9_grade:.2f} 등급")
    
    st.write("---")
    st.subheader(f"🎯 9등급 환산 ({converted_9_grade:.2f}등급) 기준 종합 지원표")
    
    # 3단계 분석 기준 안내 (구간 제한 안내 추가)
    st.markdown("""
        **[ 분석 기준 및 색상 안내 ]** (합격컷 기준)
        - <span class='legend-box' style='background-color:#fff3e0;'></span> **상향(도전)**: 내 성적보다 합격컷이 0.2 초과 ~ 0.4등급 이하 높음
        - <span class='legend-box' style='background-color:#e8f5e9;'></span> **적정(소신)**: 내 성적과 합격컷 차이가 ±0.2등급 이내
        - <span class='legend-box' style='background-color:#e3f2fd;'></span> **하향(안정)**: 내 성적보다 합격컷이 0.2 초과 ~ 0.4등급 이하 낮음
        <br><span style='font-size: 0.9em; color: #666;'>※ 지원 범위를 크게 벗어나는 대학(성적 차이가 0.4등급을 초과하는 곳)은 리스트에서 자동 제외됩니다.</span>
    """, unsafe_allow_html=True)
    
    st.write("") # 간격 띄우기

    # 계열 필터링
    filtered_df = df[df["계열"] == selected_track].copy()
    
    # 점수 차이 계산: 대학 합격컷 - 내 환산 점수
    # 예) 내 점수 3.6, 대학 3.2 -> diff = -0.4 (내 점수가 숫자가 더 큼 -> 대학 합격컷이 더 높음 -> 상향)
    filtered_df["diff"] = filtered_df["합격컷"] - converted_9_grade
    
    # 너무 높거나 낮은 대학 제외 (구간 제한: -0.4 ~ +0.4 사이의 대학만 남김)
    filtered_df = filtered_df[(filtered_df["diff"] >= -0.4) & (filtered_df["diff"] <= 0.4)].copy()
    
    # 3단계 지원 구분 판별 함수 (구간 범위 명확화)
    def assign_category(diff):
        if -0.4 <= diff < -0.2: 
            return "🚀 상향 (도전)"
        elif -0.2 <= diff <= 0.2: 
            return "✅ 적정 (소신)"
        else: 
            return "🛡️ 하향 (안정)"

    filtered_df["지원구분"] = filtered_df["diff"].apply(assign_category)
    
    # 모든 대학을 합격컷(성적 높은 순) 기준으로 정렬
    filtered_df = filtered_df.sort_values(by="합격컷")
    
    # 열 순서 재배치 (diff 열은 화면에서 숨김)
    display_cols = ["지원구분", "대학", "전형명", "전형종류", "합격컷"]
    final_df = filtered_df[display_cols]

    # 행 단위로 배경색 칠하기 (3단계)
# ... existing code ...
```

### 💡 변경된 주요 포인트
1. **분석 기준 및 색상 안내 텍스트 변경**: 단순히 "높음/낮음"이 아니라 "0.2 초과 ~ 0.4등급 이하"와 같이 학생이 직관적으로 이해할 수 있는 구체적인 범위로 설명을 바꿨습니다.
2. **데이터 필터링(`diff >= -0.4 & diff <= 0.4`) 추가**: 0.4등급 차이를 넘어가는 데이터(합격 확률이 너무 희박하거나, 성적이 너무 아까운 하향 지원)는 DataFrame에서 잘라내어 화면에 표출되지 않도록 처리했습니다. 
3. **조건부 함수 변경 (`assign_category`)**: 상향, 적정, 하향 로직이 필터링된 `-0.4 ~ +0.4`의 폐쇄된 구간 안에서 정확히 동작하도록 부등호를 교정했습니다.
