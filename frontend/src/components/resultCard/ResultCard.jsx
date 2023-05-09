import React from 'react';
import { Descriptions } from 'antd';
import styles from './ResultCard.module.css';

const renderObject = (obj) => {
  return Object.entries(obj).map(([key, value]) => {
    if (typeof value === 'object') {
      return (
        <React.Fragment key={key}>
          <Descriptions.Item label={<span className={styles.itemLabel}>{key}</span>}></Descriptions.Item>
          {renderObject(value)}
        </React.Fragment>
      );
    }

    return (
      <Descriptions.Item key={key} label={<span className={styles.itemLabel}>{key}</span>}>
        <span className={styles.itemContent}>{value}</span>
      </Descriptions.Item>
    );
  });
};

const CustomDescriptions = ({ data }) => {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Final Output</h1>
      <Descriptions bordered column={1} className={styles.descriptions}>
        {renderObject(data)}
      </Descriptions>
    </div>
  );
};

export default CustomDescriptions;
