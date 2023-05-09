import React from 'react';
import { List, Typography } from 'antd';

const { Title, Text } = Typography;

const TaskList = ({ tasks }) => {
  return (
    <List
      dataSource={tasks}
      renderItem={(task) => (
        <List.Item>
          <Title level={4}>{task.task}</Title>
          {task.dependencies.length > 0 && (
            <Text type="secondary">
              Dependencies: {task.dependencies.map((dep) => `Task ${dep.task_id}`).join(', ')}
            </Text>
          )}
        </List.Item>
      )}
    />
  );
};

export default TaskList;
