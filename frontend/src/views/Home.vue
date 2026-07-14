<template>
  <section class="page page-home">
    <div class="hero panel-card">
      <p class="eyebrow">VibeMap</p>
      <h1>지역 행사와 익명 커뮤니티를 하나의 흐름으로 묶는 초기 화면</h1>
      <p class="hero-copy">
        게시판, 행사 데이터, 챗봇을 같은 정보 구조로 다루기 위한 프론트엔드 베이스를 먼저 잡아둡니다.
      </p>

      <div class="hero-actions">
        <RouterLink class="button button-primary" to="/board">게시판 보러가기</RouterLink>
        <RouterLink class="button button-secondary" to="/events">행사 보기</RouterLink>
      </div>
    </div>

    <div class="feature-grid">
      <article class="panel-card feature-card">
        <p class="eyebrow">익명 게시판</p>
        <h2>비밀번호 기반 CRUD</h2>
        <p>회원가입 없이 게시글과 댓글을 관리하는 흐름을 우선 반영합니다.</p>
      </article>

      <article class="panel-card feature-card">
        <p class="eyebrow">행사 데이터</p>
        <h2>JSON 원본 연동</h2>
        <p>축제 데이터는 API가 아닌 원본 JSON 응답을 전제로 화면 구조를 구성합니다.</p>
      </article>

      <article class="panel-card feature-card">
        <p class="eyebrow">챗봇 UI</p>
        <h2>플로팅 대화 진입점</h2>
        <p>모바일 환경에서 빠르게 접근 가능한 대화형 진입점을 미리 마련합니다.</p>
      </article>
    </div>
  </section>
</template>