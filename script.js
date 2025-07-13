// 파일 업로드 기능
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const materialsList = document.getElementById('materialsList');

    // 드래그 앤 드롭
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.style.background = '#f8f9fa';
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.style.background = 'white';
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.style.background = 'white';
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    // 클릭으로 파일 선택
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function(e) {
        handleFiles(e.target.files);
    });

    // 파일 처리
    function handleFiles(files) {
        Array.from(files).forEach(file => {
            // 실제로는 서버에 업로드
            console.log('업로드된 파일:', file.name);
            showNotification(`${file.name} 업로드 완료!`);
        });
    }

    // 알림 표시
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #27ae60;
            color: white;
            padding: 1rem;
            border-radius: 5px;
            z-index: 10000;
        `;
        document.body.appendChild(notification);
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // 예시 강의자료 로드
    loadMaterials();
});

// 강의자료 목록 로드
function loadMaterials() {
    const materials = [
        {
            name: '마케팅 전략 기초.pdf',
            size: '2.5MB',
            date: '2024-01-15'
        },
        {
            name: '디지털 마케팅 실무.pptx',
            size: '5.2MB',
            date: '2024-01-10'
        },
        {
            name: '브랜드 마케팅 가이드.pdf',
            size: '3.1MB',
            date: '2024-01-05'
        }
    ];

    const materialsList = document.getElementById('materialsList');
    if (!materialsList) return;

    const materialsHTML = materials.map(material => `
        <div class="material-item">
            <div class="material-info">
                <h4>${material.name}</h4>
                <p>${material.size} • ${material.date}</p>
            </div>
            <a href="#" class="btn" onclick="downloadFile('${material.name}')">
                <i class="fas fa-download"></i> 다운로드
            </a>
        </div>
    `).join('');

    materialsList.innerHTML = materialsHTML;
}

// 파일 다운로드
function downloadFile(filename) {
    // 실제로는 서버에서 파일 다운로드
    console.log('다운로드:', filename);
    showNotification(`${filename} 다운로드 시작!`);
}

// 부드러운 스크롤
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
}); 