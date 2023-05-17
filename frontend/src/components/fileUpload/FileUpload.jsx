import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Card, Upload, message } from "antd";
import { InboxOutlined } from "@ant-design/icons";
import "./FileUpload.css";

const { Dragger } = Upload;

const FileUploadWindow = ({ fileUploaded, setFileUploaded, onUploadSuccess }) => {
  const onDropHandler = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];

    // Create a new FormData object and append the file to it
    const formData = new FormData();
    formData.append("file", file);

    try {
      // Send a POST request to the '/upload' route with the FormData object
      const response = await fetch("http://127.0.0.1:8000/api/file-upload", {
        method: "POST",
        body: formData,
      });

      // Check if the response is ok, then handle the response data
      if (response.ok) {
        const data = await response.json();
        console.log("File uploaded successfully!", data);
        setFileUploaded(true);
        onUploadSuccess();
      } else {
        // Handle non-200 response
        throw new Error("File upload failed");
      }
    } catch (error) {
      console.error(error);
      message.error("File upload failed. Please try connecting to server.");
    }
  }, [onUploadSuccess, setFileUploaded]);

  const { getRootProps, getInputProps } = useDropzone({ onDrop: onDropHandler });

  const props = {
    name: "file",
    multiple: false,
    accept: "application/pdf",
    showUploadList: false,
    beforeUpload: () => false,
    customRequest: () => {},
    onChange(info) {
      const { status } = info.file;
      if (status === "done") {
        message.success(`${info.file.name} file uploaded successfully.`);
      } else if (status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
  };

  return (
    <div className="file-upload-window" {...getRootProps()}>
      <h1 className="dropbox-header">JobHive 🐝 Demo</h1>
      <input {...getInputProps()} />
      <Dragger className="dragger" {...props}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">Drop your resume here</p>
        <p className="ant-upload-hint">or click to select a file (PDF only)</p>
      </Dragger>
      {fileUploaded && (
        <p className="file-upload-success">File uploaded successfully!</p>
      )}
    </div>
  );
};

export default FileUploadWindow;
