import React from 'react';
import { Card, Typography, List } from 'antd';

const { Title, Paragraph } = Typography;

function ChildSummaryRenderer({ data }) {
  const { context, task, child_summary } = data;
  const summaryItems = child_summary
    .split(/\n\n+/) // split into items using 2 or more newline characters
    .filter(item => !item.match(/^(working memory:|\[empty\])/i) && item.trim() !== '') // filter out unwanted items
    .map(item => <li key={item}>{item.trim()}</li>); // create list item for each summary item

  return (
    <Card>
      <Title level={5}>Task:</Title>
      <Paragraph>{task.split(/\n+/).join(' ')}</Paragraph>
      <Title level={5}>Agents:</Title>
      <List
        bordered
        dataSource={summaryItems}
        renderItem={item => <List.Item>{item}</List.Item>}
      />
    </Card>
  );
}

export default ChildSummaryRenderer;
