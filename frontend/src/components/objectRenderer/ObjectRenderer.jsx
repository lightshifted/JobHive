// Renders the values of agent generated objects containing the keys context, task, and results.
import { List, Card, Typography } from 'antd';

const { Title, Paragraph } = Typography;

const ObjectRenderer = ({ data }) => {
    console.log("ObjectRenderer data: ", data)
  const renderObject = () => {
    return (
      <div>
        <Title level={5}>Results:</Title>
        {data.results.split('\n').map((line, index) => (
          <Paragraph key={index}>{line}</Paragraph>
        ))}
      </div>
    )
  };

  return (
    <List.Item className="agent-response-list-item">
      <Card className="agent-response-inner-card">
        {renderObject()}
      </Card>
    </List.Item>
  );
};

export default ObjectRenderer;
