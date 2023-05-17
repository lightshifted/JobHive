import React from 'react';
import { Typography, List, Descriptions, Card } from 'antd';

const { Title } = Typography;

const WebsiteCard = ({ data }) => {
  const { speak, result } = data;

  const hasValidKeys = result.every(
    (item) => item.job_title !== undefined && item.company !== undefined && item.url !== undefined
  );

  return (
    <div>
      <Title level={5}>{speak}</Title>
      {hasValidKeys ? (
        <List size="large" bordered dataSource={result}>
          {result.map((item, index) => (
            <List.Item key={index}>
              <Descriptions column={1} bordered>
                <Descriptions.Item label="Job Title">
                  {item.job_title}
                </Descriptions.Item>
                <Descriptions.Item label="Company">
                  {item.company}
                </Descriptions.Item>
                <Descriptions.Item label="URL">
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {item.url}
                  </a>
                </Descriptions.Item>
              </Descriptions>
            </List.Item>
          ))}
        </List>
      ) : (
        <Title level={4}>
          No Dictionary Keys Found
        </Title>
      )}
    </div>
  );
};

const WebsiteCardContainer = ({ data }) => {
  return (
    <List.Item className="agent-response-list-item">
      <Card className="agent-response-inner-card">
        <WebsiteCard data={data} />
      </Card>
    </List.Item>
  );
};

export default WebsiteCardContainer;
