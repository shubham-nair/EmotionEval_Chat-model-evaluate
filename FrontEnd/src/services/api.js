export async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('http://127.0.0.1:8000/evaluate/file', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('上传失败');
  }

  return await response.json();
}
