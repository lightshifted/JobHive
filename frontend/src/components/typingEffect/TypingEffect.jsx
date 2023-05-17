import React, { useEffect, useRef } from 'react';
import Typography from 'antd/es/typography';
import Typed from 'typed.js';
import { Spin } from 'antd';

const { Text } = Typography;

const TypedText = ({ strings }) => {
  const textElement = useRef(null);
  let typed;

  useEffect(() => {
    const options = {
      strings,
      typeSpeed: .5,
      backSpeed: 0,
      loop: false,
      showCursor: false,
    };
    typed = new Typed(textElement.current, options);

    return () => {
      typed.destroy();
    };
  }, [strings]);

  return (
    <Text ref={textElement} />
  );
};

export default TypedText;

