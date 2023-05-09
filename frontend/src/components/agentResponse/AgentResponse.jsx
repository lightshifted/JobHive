import React, { useEffect, useRef, useState } from 'react';
import { List, Card, Typography, Spin } from 'antd';
import { ApiOutlined, BugTwoTone } from '@ant-design/icons';
import ListRenderer from '../listRenderer/ListRenderer';
import MemoryRenderer from '../memoryRenderer/MemoryRenderer';
import ChildSummaryRenderer from '../childSummaryRenderer/ChildSummaryRenderer';
import ObjectRenderer from '../objectRenderer/ObjectRenderer';
import TaskList from '../taskList/TaskList';
import ResultCard from '../resultCard/ResultCard';
import { Descriptions } from 'antd';
import './AgentResponse.css';

const { Title, Text, Paragraph } = Typography;

const AgentResponse = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const listRef = useRef(null);

  // Websocket connection
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

  const renderJobWebsites = (data) => {
    const { speak, result } = data;
  
    if (!result) {
      return null;
    }
  
    const isResultArray = Array.isArray(result);
    const containsDictionaries = isResultArray && result.every(
      (item) => item.job_title !== undefined && item.company !== undefined && item.url !== undefined
    );
    const containsStrings = isResultArray && result.every((item) => typeof item === 'string');
  
    return (
      <div>
        <Title level={5}>{speak}</Title>
        {containsDictionaries ? (
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
        ) : containsStrings ? (
          <List size="large" bordered dataSource={result}>
            {result.map((item, index) => (
              <List.Item key={index}>
                <a href={item} target="_blank" rel="noopener noreferrer">
                  {item}
                </a>
              </List.Item>
            ))}
          </List>
        ) : (
          <Typography.Title level={4}>
            [[END]]
          </Typography.Title>
        )}
      </div>
    );
  };
  
  
  

  const renderRelevantMemories = (data) => {
    const items = [];
  
    if (data.context) {
      items.push(data.context);
    }
  
    if (data.task) {
      items.push(data.task);
    }
  
    if (data.relevant_memories) {
      items.push(data.relevant_memories);
    }
  
    return (
      <>
        {items.map((item, index) => (
          <div key={index}>
            <Paragraph>{item}</Paragraph>
          </div>
        ))}
      </>
    );
  };

  return (
    <Card className="agent-response-card">
      <List
  className="agent-response-list"
  dataSource={messages}
  renderItem={(item) => {
    if (item.memory_content) {
      return (
        <MemoryRenderer content={item.memory_content} />
      );
    } else if (item.json?.result && item.json?.speak && !item.json?.result["Task 4"]) {
      return (
        <List.Item className="agent-response-list-item">
          <Card className="agent-response-inner-card">
            {renderJobWebsites(item.json)}
          </Card>
        </List.Item>
      );
    } else if (item.items) {
      return (
        <ListRenderer data={item} />
      );
    } else if (item.relevant_memories) {
      return (
        <List.Item className="agent-response-list-item">
          <Card className="agent-response-inner-card">
            {renderRelevantMemories(item)}
          </Card>
        </List.Item>
      );
    } else if (item.child_summary) {
      return (
        <ChildSummaryRenderer data={item} />
      );
    } else if (item.json?.result && item.json?.speak && item.json?.result["Task"]) {
      console.log("conditions met")
      return (<ResultCard data={item.json} />);

    }
    else  {
      return null;
    }
  }}
  ref={listRef}
/>
    </Card>
  );
};

export default AgentResponse;