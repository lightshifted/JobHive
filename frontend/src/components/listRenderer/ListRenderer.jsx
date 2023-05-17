import React from 'react';
import { Typography, List, Card } from 'antd';

const { Title } = Typography;

function ListRenderer(props) {
  const { data } = props;
  const { items } = data;
  
  return (
    <List.Item className="agent-response-list-item">
      <Card className="agent-response-inner-card">
        <div>
          <Title level={5}>List of Items:</Title>
          <ul>
            {items.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      </Card>
    </List.Item>
  );
}

export default ListRenderer;