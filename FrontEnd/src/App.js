// src/App.js
import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import SummaryTable from './components/SummaryTable';
import DetailTable from './components/DetailTable';
import { uploadFile } from './services/api';

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleUpload = async (file) => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await uploadFile(file);
      setResult(res);
    } catch (err) {
      setError(err.message || '分析失败');
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: 40, maxWidth: 900, margin: 'auto' }}>
      <h2>Model Judge API 前端演示</h2>
      <FileUploader onUpload={handleUpload} />
      {loading && <div>文件上传/分析中，请稍候...</div>}
      {error && <div style={{ color: 'red' }}>错误：{error}</div>}
      {result && (
        <>
          <SummaryTable summary={result.summary} />
          <DetailTable detail={result.detail} />
        </>
      )}
    </div>
  );
}

export default App;
