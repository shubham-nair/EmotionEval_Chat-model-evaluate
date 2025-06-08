import React, { useState } from 'react';
import { uploadFile } from './services/api';

export default function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleUpload = async (file) => {
    try {
      const res = await uploadFile(file);
      setResult(res);
      setError('');
    } catch (err) {
      setError(err.message || '上传失败');
      setResult(null);
    }
  };

  return (
    <div>
      <FileUploader onUpload={handleUpload} />
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {result && <div>{JSON.stringify(result)}</div>}
    </div>
  );
}

function FileUploader({ onUpload }) {
  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) onUpload(file);
  };
  return <input type="file" accept=".json,.csv" onChange={handleUpload} />;
}
