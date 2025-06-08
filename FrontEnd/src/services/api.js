export async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('/evaluate/file', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`上传失败，状态码 ${response.status}`);
  }

  return response.json();
}
