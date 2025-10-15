document.getElementById("uploadForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const description = document.getElementById("description").value;
  const price = document.getElementById("price").value;
  const file = document.getElementById("file").files[0];

  if (!file) {
    alert("Vui lòng chọn file CSV!");
    return;
  }

  alert(`✅ Dataset "${name}" đã được tải lên tạm thời (chưa kết nối API).`);
});

