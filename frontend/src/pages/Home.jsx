import { useState } from "react";
import AgentResponse from "../components/agentResponse/AgentResponse";
import FileUploadWindow from "../components/fileUpload/FileUpload";
import { Button } from 'antd';

const Home = () => {
    const [fileUploaded, setFileUploaded] = useState(false);
    const [showComponent, setShowComponent] = useState("upload");

    const handleFileUploadSuccess = () => {
        setFileUploaded(true);
        setShowComponent("response");
    };

    const handleComponentSwitch = () => {
        setShowComponent(showComponent === "upload" ? "response" : "upload");
    };

    return (
        <div>
            <Button onClick={handleComponentSwitch}>
                {showComponent === "upload" ? "Show Agent Response" : "Show File Upload Window"}
            </Button>
            {showComponent === "response" && <AgentResponse />}
            {showComponent === "upload" && (
                <FileUploadWindow
                    fileUploaded={fileUploaded}
                    setFileUploaded={setFileUploaded}
                    onUploadSuccess={handleFileUploadSuccess}
                />
            )}
        </div>
    );
}

export default Home;
