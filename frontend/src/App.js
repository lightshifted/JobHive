import React, { useEffect, useState } from 'react';
import { List, Card, Typography, Spin } from 'antd';
import { ApiOutlined } from '@ant-design/icons';

const { Title } = Typography;


const App = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    const ws = new WebSocket("ws://localhost:2000/");

    ws.addEventListener("open", (event) => {
      console.log("WebSocket connection opened:", event);
      setLoading(false);
    });

    ws.addEventListener("message", (event) => {
      console.log("WebSocket received message:", event.data);
      const message = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, message]);
    });

    ws.addEventListener("error", (event) => {
      console.log("WebSocket encountered an error:", event);
      setLoading(false);
    });

    ws.addEventListener("close", (event) => {
      console.log("WebSocket connection closed:", event);
      console.log("Close code:", event.code);
      console.log("Close reason:", event.reason);
      setLoading(false);
    });

    return () => {
      ws.close();
    };
  }, []);

  return (
    <Card>
      <Title level={2}>
        <ApiOutlined /> WebSocket Test
      </Title>
      {loading ? (
        <Spin />
      ) : (
        <List
          dataSource={messages}
          renderItem={(item) => (
            <List.Item>
              <Typography.Text>{JSON.stringify(item)}</Typography.Text>
            </List.Item>
          )}
        />
      )}
    </Card>
  );
};

export default App;
