import React, { useState } from 'react';
import { Upload, Button, Table, Typography, Alert, Space, message, Card, Divider } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import { uploadFile } from './services/api';
// 如果没装，可以注释掉下面这两行和 <BarChart> 部分
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, LabelList } from 'recharts';

const { Title } = Typography;

const summaryColumns = [
  { title: '模型', dataIndex: 'model_version', key: 'model_version', align: 'center' },
  { title: '平均F1', dataIndex: 'f1_avg', key: 'f1_avg', align: 'center', render: val => val != null ? val.toFixed(4) : '--' },
  { title: '平均Precision', dataIndex: 'precision_avg', key: 'precision_avg', align: 'center', render: val => val != null ? val.toFixed(4) : '--' },
  { title: '平均Recall', dataIndex: 'recall_avg', key: 'recall_avg', align: 'center', render: val => val != null ? val.toFixed(4) : '--' },
  { title: '平均情绪提升', dataIndex: 'emotion_slope', key: 'emotion_slope', align: 'center', render: val => val != null ? val.toFixed(4) : '--' },
  { title: '累计增益', dataIndex: 'cumulative_gain', key: 'cumulative_gain', align: 'center', render: val => val != null ? val.toFixed(4) : '--' },
  { title: '会话数', dataIndex: 'count', key: 'count', align: 'center' },
];

const detailColumns = [
  { title: 'Session ID', dataIndex: 'session_id', key: 'session_id', align: 'center' },
  { title: '模型', dataIndex: 'model_version', key: 'model_version', align: 'center' },
  { title: 'F1', dataIndex: 'f1_avg', key: 'f1_avg', align: 'center', render: val => val?.toFixed(4) },
  { title: 'Precision', dataIndex: 'precision_avg', key: 'precision_avg', align: 'center', render: val => val?.toFixed(4) },
  { title: 'Recall', dataIndex: 'recall_avg', key: 'recall_avg', align: 'center', render: val => val?.toFixed(4) },
  { title: '开始情绪', dataIndex: 'start_sentiment', key: 'start_sentiment', align: 'center', render: val => val?.toFixed(3) },
  { title: '结束情绪', dataIndex: 'end_sentiment', key: 'end_sentiment', align: 'center', render: val => val?.toFixed(3) },
  { title: '情绪提升', dataIndex: 'emotion_slope', key: 'emotion_slope', align: 'center', render: val => val?.toFixed(3) },
  { title: '累计增益', dataIndex: 'cumulative_gain', key: 'cumulative_gain', align: 'center', render: val => val?.toFixed(3) },
  { title: '平均Bot情绪', dataIndex: 'avg_bot_sentiment', key: 'avg_bot_sentiment', align: 'center', render: val => val?.toFixed(3) },
  { title: '轮次', dataIndex: 'turns', key: 'turns', align: 'center' },
];

// 图表字段
const chartMetrics = [
  { key: 'f1_avg', name: '平均F1', color: '#4a90e2' },
  { key: 'precision_avg', name: 'Precision', color: '#8bc34a' },
  { key: 'recall_avg', name: 'Recall', color: '#ffc107' },
  { key: 'emotion_slope', name: '情绪提升', color: '#ff6f91' },
];

export default function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [showAll, setShowAll] = useState(false);

  const handleUpload = async ({ file, onSuccess, onError }) => {
    setLoading(true);
    setError('');
    setResult(null);
    setShowAll(false);
    try {
      const res = await uploadFile(file);
      setResult(res);
      onSuccess('ok');
      message.success('上传分析成功！');
    } catch (err) {
      setError(err.message || '上传失败');
      onError?.(err);
    } finally {
      setLoading(false);
    }
  };

  const detailData = result?.detail || [];

  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(120deg,#f8fafd 65%,#e3e8fd 100%)',
        padding: '42px 0',
      }}
    >
      <Card
        style={{
          maxWidth: 1180,
          width: '95%',
          margin: '32px auto 12px',
          borderRadius: 32,
          boxShadow: '0 8px 32px #e8eaef',
          padding: '46px 26px 36px 26px',
          background: '#fff',
          border: 'none'
        }}
        bodyStyle={{ padding: 0 }}
      >
        <Title
          level={1}
          style={{
            textAlign: 'center',
            fontWeight: 900,
            marginBottom: 34,
            fontSize: 36,
            color: '#233556',
            letterSpacing: 1.5
          }}
        >
          多模型对话自动评测平台
        </Title>

        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 36 }}>
          <Upload
            accept=".json,.csv"
            showUploadList={false}
            customRequest={handleUpload}
            disabled={loading}
          >
            <Button
              type="primary"
              size="large"
              icon={<UploadOutlined />}
              loading={loading}
              style={{
                borderRadius: 14,
                padding: '0 38px',
                height: 48,
                fontSize: 20,
                background: 'linear-gradient(90deg,#5c9afe,#7676ff 80%)',
                borderColor: '#3366ff',
              }}
            >
              上传文件
            </Button>
          </Upload>
        </div>

        {error && (
          <Alert
            message={error}
            type="error"
            showIcon
            style={{
              margin: '32px 0',
              fontSize: 17,
              borderRadius: 10,
            }}
          />
        )}

        {result && (
          <Space direction="vertical" size={46} style={{ width: '100%' }}>
            {result.summary && (
              <>
                <Divider orientation="left" orientationMargin="0" style={{ fontWeight: 700, fontSize: 20 }}>
                  汇总统计
                </Divider>
                <Table
                  columns={summaryColumns}
                  dataSource={result.summary}
                  rowKey={row => row.model_version}
                  bordered
                  pagination={false}
                  style={{
                    background: '#f7faff',
                    borderRadius: 18,
                    fontSize: 17,
                    boxShadow: '0 1px 8px #eef1f6',
                  }}
                />

                {/* 柱状图 */}
                <div style={{ width: '100%', minHeight: 320, marginTop: 20, background: '#f8fafd', borderRadius: 16 }}>
                  <ResponsiveContainer width="100%" height={320}>
                    <BarChart
                      data={result.summary}
                      margin={{ top: 30, right: 40, left: 10, bottom: 18 }}
                    >
                      <XAxis dataKey="model_version" tick={{ fontSize: 16 }} />
                      <YAxis tick={{ fontSize: 16 }} />
                      <Tooltip />
                      <Legend />
                      {chartMetrics.map(metric => (
                        <Bar
                          key={metric.key}
                          dataKey={metric.key}
                          name={metric.name}
                          barSize={30}
                          radius={[8, 8, 0, 0]}
                          fill={metric.color}
                        >
                          <LabelList dataKey={metric.key} position="top" formatter={v => v?.toFixed(2)} />
                        </Bar>
                      ))}
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </>
            )}

            {/* 明细面板，默认只展示前6条，可点展开查看更多 */}
            <Divider orientation="left" orientationMargin="0" style={{ fontWeight: 700, fontSize: 20 }}>
              明细结果
            </Divider>
            <div style={{ background: '#f8fafd', borderRadius: 16, minHeight: 90 }}>
              <Table
                columns={detailColumns}
                dataSource={showAll ? detailData : detailData.slice(0, 6)}
                rowKey={row => row.session_id + '-' + row.model_version}
                bordered
                scroll={{ x: 'max-content' }}
                pagination={showAll ? { pageSize: 12 } : false}
                style={{
                  background: '#fff',
                  borderRadius: 18,
                  fontSize: 16,
                  boxShadow: '0 1px 7px #eef1f6',
                }}
                size="middle"
              />
              {detailData.length > 6 && (
                <div style={{ textAlign: 'center', margin: '18px 0 4px 0' }}>
                  <Button
                    size="small"
                    type="link"
                    style={{ fontSize: 17, color: '#4a90e2', letterSpacing: 1 }}
                    onClick={() => setShowAll(!showAll)}
                  >
                    {showAll ? '收起明细' : `展开全部（${detailData.length}条）`}
                  </Button>
                </div>
              )}
            </div>
          </Space>
        )}
      </Card>
      <div style={{ textAlign: 'center', marginTop: 34, color: '#adb2be', fontSize: 15 }}>
        © {new Date().getFullYear()} Model Judge | Powered by Ant Design & Recharts
        <span style={{ marginLeft: 16 }}>
          <a href="https://github.com/Islene888/EmotionEval_Chat-model-evaluate" target="_blank" rel="noopener noreferrer" style={{ color: '#5672e3' }}>
            GitHub
          </a>
        </span>
      </div>
    </div>
  );
}
