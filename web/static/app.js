// Upload form (nếu có trên trang)
const uploadForm = document.getElementById("uploadForm");
if (uploadForm) {
  uploadForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const name = document.getElementById("name").value.trim();
    const description = document.getElementById("description").value.trim();
    const price = parseFloat(document.getElementById("price").value);
    const file = document.getElementById("file").files[0];
    
    // Validation
    let hasError = false;
    clearFieldError('name');
    clearFieldError('price');
    clearFieldError('file');
    
    if (!name) {
      showFieldError('name', 'Vui lòng nhập tên dataset');
      hasError = true;
    }
    
    if (isNaN(price) || price < 0) {
      showFieldError('price', 'Giá phải là số dương');
      hasError = true;
    }
    
    if (!file) {
      showFieldError('file', 'Vui lòng chọn file CSV');
      hasError = true;
    } else if (!file.name.toLowerCase().endsWith('.csv')) {
      showFieldError('file', 'Chỉ chấp nhận file CSV');
      hasError = true;
    }
    
    if (hasError) return;
    
    const token = localStorage.getItem("token");
    if (!token) {
      showToast("Vui lòng đăng nhập trước khi upload", "error");
      setTimeout(() => {
        window.location.href = "/ui/login";
      }, 1000);
      return;
    }
    
    const submitBtn = uploadForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Đang tải lên...';
    
    const fd = new FormData();
    fd.append("title", name);
    fd.append("description", description);
    fd.append("price", price);
    fd.append("file", file);
    
    fetch(`/datasets/upload`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: fd,
    })
      .then((r) => r.json())
      .then((d) => {
        if (d.detail) {
          showToast(`Lỗi: ${d.detail}`, "error");
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
        } else {
          showToast(`✅ Đã tạo dataset #${d.id}`, "success");
          setTimeout(() => {
            window.location.href = "/ui/my-datasets";
          }, 1000);
        }
      })
      .catch((e) => {
        showToast("Lỗi upload: " + e.message, "error");
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
      });
  });
}

// Dashboard summary loader
async function loadSummary() {
  const sumUsers = document.getElementById("sumUsers");
  const sumDatasets = document.getElementById("sumDatasets");
  const sumTxs = document.getElementById("sumTxs");
  const latestList = document.getElementById("latestList");
  if (!sumUsers || !sumDatasets || !sumTxs || !latestList) return;

  try {
    const res = await fetch(`/datasets/stats/summary`);
    const data = await res.json();
    sumUsers.textContent = data.users ?? 0;
    sumDatasets.textContent = data.datasets ?? 0;
    sumTxs.textContent = data.transactions ?? 0;
    latestList.innerHTML = "";
    (data.latest || []).forEach((d) => {
      const li = document.createElement("li");
      li.className = 'list-item';
      const title = document.createElement('a');
      title.href = `/ui/dataset?id=${d.id}`;
      title.className = 'list-title';
      title.style.textDecoration = 'none';
      title.style.color = '#0b5fff';
      title.textContent = d.title;
      const meta = document.createElement('div');
      meta.className = 'list-meta';
      const price = document.createElement('span');
      price.className = 'badge badge-info';
      price.textContent = `${d.price ?? 0} VNĐ`;
      const date = document.createElement('span');
      date.className = 'list-date';
      date.textContent = d.created_at ? new Date(d.created_at).toLocaleDateString('vi-VN') : '';
      meta.appendChild(price);
      meta.appendChild(date);
      li.appendChild(title);
      li.appendChild(meta);
      latestList.appendChild(li);
    });
  } catch (e) {
    console.error(e);
  }
}
loadSummary();

// Advanced search form
const searchForm = document.getElementById("searchForm");
let currentPage = 1;
async function runSearch(pageOverride) {
  const results = document.getElementById("results");
  if (!searchForm || !results) return;
  const table = document.getElementById("resultsTable");
  const tbody = table ? table.querySelector('tbody') : null;
  const loading = document.getElementById('resultsLoading');
  const empty = document.getElementById('resultsEmpty');
  const q = document.getElementById("q").value || "";
  const min_price = document.getElementById("min_price").value;
  const max_price = document.getElementById("max_price").value;
  const owner_id = document.getElementById("owner_id").value;
  const start_date = document.getElementById("start_date").value;
  const end_date = document.getElementById("end_date").value;
  const sort_by = document.getElementById("sort_by").value;
  const sort_dir = document.getElementById("sort_dir").value;
  const page_size = document.getElementById("page_size").value || 10;
  if (pageOverride) currentPage = pageOverride;

  const params = new URLSearchParams();
  if (q) params.append("q", q);
  if (min_price) params.append("min_price", min_price);
  if (max_price) params.append("max_price", max_price);
  if (owner_id) params.append("owner_id", owner_id);
  if (start_date) params.append("start_date", start_date);
  if (end_date) params.append("end_date", end_date);
  if (sort_by) params.append("sort_by", sort_by);
  if (sort_dir) params.append("sort_dir", sort_dir);
  params.append("page", currentPage);
  params.append("page_size", page_size);

  if (loading) loading.style.display = 'block';
  if (empty) empty.style.display = 'none';
  if (tbody) tbody.innerHTML = '';
  try {
    const res = await fetch(`/datasets/search?${params.toString()}`);
    const data = await res.json();
    const items = data.items || [];
    if (!items.length) {
      if (empty) empty.style.display = 'block';
      return;
    }
    if (tbody) {
      const rows = items.map(d => `
        <tr>
          <td><a href="/ui/dataset?id=${d.id}" style="text-decoration: none; color: #0b5fff; font-weight: 600;">${d.title}</a></td>
          <td>${(d.description || '').substring(0, 100)}${(d.description || '').length > 100 ? '...' : ''}</td>
          <td><span class="badge badge-info">${d.price ?? 0} VNĐ</span></td>
          <td>${d.created_at ? new Date(d.created_at).toLocaleDateString('vi-VN') : ''}</td>
          <td><a href="/ui/dataset?id=${d.id}" class="btn btn-primary" style="text-decoration: none; padding: 6px 12px; font-size: 13px;">Xem chi tiết</a></td>
        </tr>
      `).join('');
      tbody.innerHTML = rows;
    }
  } catch (e) {
    showToast('Lỗi tải dữ liệu tìm kiếm', 'error');
  }
  finally { if (loading) loading.style.display = 'none'; }
}

if (searchForm) {
  searchForm.addEventListener("submit", function (e) {
    e.preventDefault();
    currentPage = 1;
    runSearch(1);
  });
  const prev = document.getElementById("prevPage");
  const next = document.getElementById("nextPage");
  if (prev) prev.addEventListener("click", () => { currentPage = Math.max(1, currentPage - 1); runSearch(currentPage); });
  if (next) next.addEventListener("click", () => { currentPage += 1; runSearch(currentPage); });
}

// Toast helper
function showToast(message, type) {
  let el = document.getElementById('appToast');
  if (!el) {
    el = document.createElement('div');
    el.id = 'appToast';
    el.className = 'toast';
    document.body.appendChild(el);
  }
  el.className = `toast show ${type || ''}`;
  el.textContent = message;
  setTimeout(() => { el.className = 'toast'; }, 2200);
}

// Form validation helper
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showFieldError(fieldId, message) {
  const field = document.getElementById(fieldId);
  if (!field) return;
  field.style.borderColor = '#b91c1c';
  let errorDiv = document.getElementById(fieldId + '_error');
  if (!errorDiv) {
    errorDiv = document.createElement('div');
    errorDiv.id = fieldId + '_error';
    errorDiv.className = 'field-error';
    errorDiv.style.color = '#b91c1c';
    errorDiv.style.fontSize = '13px';
    errorDiv.style.marginTop = '4px';
    field.parentElement.appendChild(errorDiv);
  }
  errorDiv.textContent = message;
}

function clearFieldError(fieldId) {
  const field = document.getElementById(fieldId);
  if (field) field.style.borderColor = '';
  const errorDiv = document.getElementById(fieldId + '_error');
  if (errorDiv) errorDiv.remove();
}

// Login form
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const code = document.getElementById("code") ? document.getElementById("code").value : "";
    
    // Validation
    let hasError = false;
    clearFieldError('email');
    clearFieldError('password');
    
    if (!email) {
      showFieldError('email', 'Vui lòng nhập email');
      hasError = true;
    } else if (!validateEmail(email)) {
      showFieldError('email', 'Email không hợp lệ');
      hasError = true;
    }
    
    if (!password) {
      showFieldError('password', 'Vui lòng nhập mật khẩu');
      hasError = true;
    } else if (password.length < 6) {
      showFieldError('password', 'Mật khẩu phải có ít nhất 6 ký tự');
      hasError = true;
    }
    
    if (hasError) return;
    
    const submitBtn = loginForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Đang đăng nhập...';
    
    fetch(`/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, code }),
    })
      .then((r) => r.json())
      .then((d) => {
        if (d.access_token) {
          localStorage.setItem("token", d.access_token);
          showToast("Đăng nhập thành công", "success");
          setTimeout(() => {
            window.location.href = "/ui/dashboard";
          }, 500);
        } else {
          showToast(d.detail || "Đăng nhập thất bại", "error");
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
        }
      })
      .catch((e) => {
        showToast("Lỗi đăng nhập: " + e.message, "error");
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
      });
  });
}

// Register form
const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const username = document.getElementById("reg_username").value.trim();
    const email = document.getElementById("reg_email").value.trim();
    const password = document.getElementById("reg_password").value;
    
    // Validation
    let hasError = false;
    clearFieldError('reg_username');
    clearFieldError('reg_email');
    clearFieldError('reg_password');
    
    if (!username) {
      showFieldError('reg_username', 'Vui lòng nhập tên người dùng');
      hasError = true;
    } else if (username.length < 3) {
      showFieldError('reg_username', 'Tên người dùng phải có ít nhất 3 ký tự');
      hasError = true;
    }
    
    if (!email) {
      showFieldError('reg_email', 'Vui lòng nhập email');
      hasError = true;
    } else if (!validateEmail(email)) {
      showFieldError('reg_email', 'Email không hợp lệ');
      hasError = true;
    }
    
    if (!password) {
      showFieldError('reg_password', 'Vui lòng nhập mật khẩu');
      hasError = true;
    } else if (password.length < 6) {
      showFieldError('reg_password', 'Mật khẩu phải có ít nhất 6 ký tự');
      hasError = true;
    }
    
    if (hasError) return;
    
    const submitBtn = registerForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Đang đăng ký...';
    
    fetch(`/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    })
      .then((r) => r.json())
      .then((d) => {
        if (d.id) {
          showToast("Đăng ký thành công, mời đăng nhập", "success");
          setTimeout(() => {
            window.location.href = "/ui/login";
          }, 1000);
        } else {
          showToast(d.detail || "Đăng ký thất bại", "error");
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
        }
      })
      .catch((e) => {
        showToast("Lỗi đăng ký: " + e.message, "error");
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
      });
  });
}

// My datasets loader
async function loadMyDatasets() {
  const container = document.getElementById("myDatasetsList");
  if (!container) return;
  const token = localStorage.getItem("token");
  if (!token) {
    container.innerHTML = "Vui lòng đăng nhập để xem danh sách.";
    return;
  }
  container.innerHTML = "Đang tải...";
  try {
    const res = await fetch(`/datasets/mine`, { headers: { Authorization: `Bearer ${token}` } });
    const data = await res.json();
    if (!Array.isArray(data) || data.length === 0) {
      container.innerHTML = "Chưa có dataset nào.";
      return;
    }
    container.innerHTML = data
      .map(
        (d) =>
          `<div style="border:1px solid #d1d1d1;border-radius:8px;padding:10px;margin-bottom:8px;" data-id="${d.id}">
            <div><strong>${d.title}</strong></div>
            <div>${d.description || ""}</div>
            <div>Giá: ${d.price ?? 0}</div>
            <div>Ngày tạo: ${d.created_at || ""}</div>
            <div style="margin-top:8px;display:flex;gap:8px;">
              <button class="btnEdit" type="button">Sửa</button>
              <button class="btnDelete" type="button">Xóa</button>
            </div>
          </div>`
      )
      .join("");

    // attach handlers
    container.querySelectorAll(".btnEdit").forEach((btn) => {
      btn.addEventListener("click", async (e) => {
        const card = e.target.closest('[data-id]');
        const id = card.getAttribute('data-id');
        const newTitle = prompt("Tiêu đề mới:", card.querySelector('strong').textContent);
        if (newTitle === null) return;
        const newDesc = prompt("Mô tả mới:", card.children[1].textContent || "");
        const newPriceStr = prompt("Giá mới:", (card.children[2].textContent.replace('Giá: ', '') || '0'));
        const fd = new FormData();
        fd.append('title', newTitle);
        fd.append('description', newDesc || '');
        if (newPriceStr) fd.append('price', newPriceStr);
        const resp = await fetch(`/datasets/${id}`, { method: 'PUT', headers: { Authorization: `Bearer ${token}` }, body: fd });
        const out = await resp.json();
        if (out.detail) alert(out.detail); else { alert('Đã cập nhật'); loadMyDatasets(); }
      });
    });
    container.querySelectorAll(".btnDelete").forEach((btn) => {
      btn.addEventListener("click", async (e) => {
        const card = e.target.closest('[data-id]');
        const id = card.getAttribute('data-id');
        if (!confirm('Bạn chắc chắn muốn xóa?')) return;
        const resp = await fetch(`/datasets/${id}`, { method: 'DELETE', headers: { Authorization: `Bearer ${token}` } });
        const out = await resp.json();
        if (out.ok) { alert('Đã xóa'); loadMyDatasets(); } else { alert(out.detail || 'Xóa thất bại'); }
      });
    });
  } catch (e) {
    console.error(e);
    container.innerHTML = "Lỗi tải dữ liệu.";
  }
}
loadMyDatasets();

// Profile loader
async function loadProfile() {
  const box = document.getElementById('profileInfo');
  if (!box) return;
  const token = localStorage.getItem('token');
  if (!token) { box.innerHTML = 'Vui lòng đăng nhập.'; return; }
  try {
    const res = await fetch('/users/me', { headers: { Authorization: `Bearer ${token}` } });
    const u = await res.json();
    if (u.detail) { box.innerHTML = u.detail; return; }
    box.innerHTML = `<div><strong>ID:</strong> ${u.id}</div>
                     <div><strong>Username:</strong> ${u.username}</div>
                     <div><strong>Email:</strong> ${u.email}</div>
                     <div><strong>Role:</strong> ${u.role}</div>`;
  } catch (e) {
    box.innerHTML = 'Lỗi tải hồ sơ.';
  }
}
loadProfile();

// Change password
const changePwdForm = document.getElementById('changePwdForm');
if (changePwdForm) {
  changePwdForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    if (!token) { alert('Vui lòng đăng nhập'); return; }
    const old_password = document.getElementById('old_password').value;
    const new_password = document.getElementById('new_password').value;
    const res = await fetch('/users/me/change-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ old_password, new_password })
    });
    const out = await res.json();
    if (out.ok) alert('Đã đổi mật khẩu'); else alert(out.detail || 'Đổi mật khẩu thất bại');
  });
}

// 2FA status
async function loadTwofaStatus() {
  const s = document.getElementById('twofaStatus');
  if (!s) return;
  const token = localStorage.getItem('token');
  if (!token) { s.textContent = 'Chưa đăng nhập'; return; }
  try {
    const res = await fetch('/users/me/twofa/status', { headers: { Authorization: `Bearer ${token}` } });
    const data = await res.json();
    s.textContent = data.enabled ? '2FA: Đang bật' : '2FA: Đang tắt';
    if (!data.enabled) {
      // Thử hiển thị QR nếu đã setup trước đó
      renderTwofaQRIfAvailable();
    } else {
      const qrBox = document.getElementById('twofaQR');
      if (qrBox) qrBox.innerHTML = '';
    }
  } catch (e) {
    s.textContent = 'Không lấy được trạng thái 2FA';
  }
}
loadTwofaStatus();

// 2FA setup
const btnTwofaSetup = document.getElementById('btnTwofaSetup');
if (btnTwofaSetup) {
  btnTwofaSetup.addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    if (!token) { alert('Vui lòng đăng nhập'); return; }
    const res = await fetch('/users/me/twofa/setup', { method: 'POST', headers: { Authorization: `Bearer ${token}` } });
    const d = await res.json();
    const box = document.getElementById('twofaSetupBox');
    box.innerHTML = `
      <div>Secret: <code>${d.secret || ''}</code></div>
      <div><a href="${d.otpauth_url || '#'}" target="_blank">Liên kết cấu hình 2FA</a></div>
      <div>Quét QR dưới đây bằng Google Authenticator/1Password.</div>
    `;
    const qrBox = document.getElementById('twofaQR');
    if (qrBox) {
      qrBox.innerHTML = '<img id="twofaQRImg" alt="QR Code 2FA" style="width:180px;height:180px;border:1px solid #d1d1d1;border-radius:6px;" />';
      // Tải ảnh QR bằng fetch để đính kèm Authorization
      try {
        const resp = await fetch(`/users/me/twofa/qr?ts=${Date.now()}`, { headers: { Authorization: `Bearer ${token}` } });
        if (resp.ok) {
          const blob = await resp.blob();
          const url = URL.createObjectURL(blob);
          const img = document.getElementById('twofaQRImg');
          if (img) img.src = url;
        }
      } catch {}
    }
  });
}

async function renderTwofaQRIfAvailable() {
  const qrBox = document.getElementById('twofaQR');
  if (!qrBox) return;
  const token = localStorage.getItem('token');
  if (!token) return;
  try {
    const resp = await fetch(`/users/me/twofa/qr?ts=${Date.now()}`, { headers: { Authorization: `Bearer ${token}` } });
    if (!resp.ok) return; // chưa setup -> 400
    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);
    qrBox.innerHTML = '<img id="twofaQRImgAuto" alt="QR Code 2FA" style="width:180px;height:180px;border:1px solid #d1d1d1;border-radius:6px;" />';
    const img = document.getElementById('twofaQRImgAuto');
    if (img) img.src = url;
  } catch {}
}

// 2FA enable/disable
const btnTwofaEnable = document.getElementById('btnTwofaEnable');
const btnTwofaDisable = document.getElementById('btnTwofaDisable');
if (btnTwofaEnable) {
  btnTwofaEnable.addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    const code = document.getElementById('twofaCode').value;
    const res = await fetch(`/users/me/twofa/enable?code=${encodeURIComponent(code)}`, { method: 'POST', headers: { Authorization: `Bearer ${token}` } });
    const d = await res.json();
    if (d.enabled) { alert('Đã bật 2FA'); loadTwofaStatus(); }
    else alert(d.detail || 'Bật 2FA thất bại');
  });
}
if (btnTwofaDisable) {
  btnTwofaDisable.addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    const code = document.getElementById('twofaCode').value;
    const res = await fetch(`/users/me/twofa/disable?code=${encodeURIComponent(code)}`, { method: 'POST', headers: { Authorization: `Bearer ${token}` } });
    const d = await res.json();
    if (d.enabled === false) { alert('Đã tắt 2FA'); loadTwofaStatus(); }
    else alert(d.detail || 'Tắt 2FA thất bại');
  });
}

// Logout
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
  logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('token');
    alert('Đã đăng xuất');
    window.location.href = '/ui/login';
  });
}