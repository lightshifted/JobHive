import React from 'react';
import { List, Card, Typography } from 'antd';

const { Paragraph } = Typography;

function MemoryContent({ content }) {
  const lines = content.replace('[[MEMORY]]', '').split('\n');

  return (
    <List.Item className="agent-response-list-item">
      <Card className="agent-response-inner-card">
        {lines.map((line, index) => (
          <Paragraph key={index}>{line}</Paragraph>
        ))}
      </Card>
    </List.Item>
  );
}

export default MemoryContent;

