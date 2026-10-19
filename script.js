const menuButton = document.querySelector('.menu-button');
const navigation = document.querySelector('.primary-nav');
const regionModal = document.querySelector('#region-modal');
const regionModalClose = document.querySelector('.region-modal-close');

// 사이트에 처음 들어온 첫 화면에서만 지역 선택 창을 띄웁니다.
// 사이트 안에서 이동해 왔거나(#contact 등) 이번 방문에 이미 본 경우에는 띄우지 않습니다.
const shouldShowRegionModal = () => {
  if (window.location.hash) return false;
  try {
    if (document.referrer && new URL(document.referrer).host === window.location.host) return false;
  } catch (error) { /* 잘못된 referrer는 무시 */ }
  try {
    if (sessionStorage.getItem('regionModalSeen')) return false;
    sessionStorage.setItem('regionModalSeen', '1');
  } catch (error) { /* 저장소를 쓸 수 없으면 한 번 띄웁니다 */ }
  return true;
};

if (regionModal && regionModalClose && shouldShowRegionModal()) {
  const closeRegionModal = () => {
    regionModal.classList.add('is-closed');
    document.body.classList.remove('region-modal-open');
  };

  regionModal.classList.remove('is-closed');
  document.body.classList.add('region-modal-open');
  regionModalClose.focus();

  regionModalClose.addEventListener('click', closeRegionModal);
  regionModal.addEventListener('click', (event) => {
    if (event.target === regionModal) {
      closeRegionModal();
    }
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !regionModal.classList.contains('is-closed')) {
      closeRegionModal();
    }
  });
}

menuButton.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!isOpen));
  menuButton.setAttribute('aria-label', isOpen ? '메뉴 열기' : '메뉴 닫기');
  navigation.classList.toggle('open', !isOpen);
  document.body.classList.toggle('menu-open', !isOpen);
});

navigation.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', '메뉴 열기');
    navigation.classList.remove('open');
    document.body.classList.remove('menu-open');
  });
});

const gradeData = {
  elementary: {
    label: 'FOUNDATION',
    title: '수학의 기초 체력을 만듭니다',
    description: '연산의 정확도와 교과 개념을 다지고, 풀이 과정을 자신의 말로 설명하는 습관을 만듭니다.',
    points: ['교과 개념과 연산 습관', '서술형 풀이 과정 연습', '중등 수학을 위한 사고력']
  },
  middle: {
    label: 'CORE CONCEPT',
    title: '개념을 연결하고 내신을 다집니다',
    description: '단원별 핵심 개념을 연결해 이해하고, 학교 시험 유형에 맞춰 풀이 정확도와 속도를 높입니다.',
    points: ['학교별 내신 진도 관리', '취약 단원 집중 보완', '고등 수학 기초 연결']
  },
  high: {
    label: 'EXAM STRATEGY',
    title: '목표에 맞는 전략을 세웁니다',
    description: '내신과 수능 목표를 함께 고려해 개념, 기출, 실전 문제를 단계적으로 학습합니다.',
    points: ['내신과 모의고사 병행', '기출 분석과 오답 관리', '학생별 입시 목표 설계']
  }
};

const gradePanel = document.querySelector('.grade-panel');
document.querySelectorAll('.grade-tabs button').forEach((tab) => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.grade-tabs button').forEach((button) => button.setAttribute('aria-selected', 'false'));
    tab.setAttribute('aria-selected', 'true');
    const grade = gradeData[tab.dataset.grade];
    gradePanel.innerHTML = `<small>${grade.label}</small><h3>${grade.title}</h3><p>${grade.description}</p><ul>${grade.points.map((point) => `<li>${point}</li>`).join('')}</ul>`;
  });
});

const revealObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));
document.querySelector('#year').textContent = new Date().getFullYear();
