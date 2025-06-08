import React, { useRef } from 'react';
import { uploadFile } from '../services/api';

const FileUploader = ({ onResult }) => {
  const fileInput = useRef(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const result = await uploadFile(file);
      onResult(result);  // 将后端返回结果传递给App
    } catch (err) {
      alert('上传失败，请检查后端服务和文件格式');
    }
  };

  return (
    <div style={{ marginBottom: 20 }}>
      <input
        type="file"
        accept=".json,.csv"
        ref={fileInput}
        onChange={handleUpload}
      />
    </div>
  );
};

export default FileUploader;
