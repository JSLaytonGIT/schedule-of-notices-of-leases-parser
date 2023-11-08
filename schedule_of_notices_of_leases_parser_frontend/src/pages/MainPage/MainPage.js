import React, { useState } from 'react';
import api from '../../utils/apiConfig';
import Loader from 'react-loaders'
import JsonView from '@uiw/react-json-view';
import { vscodeTheme } from '@uiw/react-json-view/vscode';
import './MainPage.scss';

const MainPage = () => {
    const [file, setFile] = useState(null);
    const [jsonResponse, setJsonResponse] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isResponse, setIsResponse] = useState(false);

    const handleFile = (event) => {
        const file = event.target.files[0];
        setFile(file);
    };

    const handleGo = async () => {
        console.log("Go clicked");
        setIsLoading(true);
        if (file) {
            try {
                console.log(file)
                const formData = new FormData();
                formData.append('file', file);
                Object.fromEntries(formData.entries())
                const response = await api.post('/api/schedule_of_notices_of_leases_parser', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                console.log("RESPONSE:", response.data)
                setJsonResponse(response.data)

            } catch (error) {
                console.error(error);
            } finally {
                setIsResponse(true);
                setIsLoading(false);
            }
        } else {
            alert('Please select a PDF file before uploading.');
            setIsLoading(false);
        }
    }

    const handleDownload = () => {
        if (jsonResponse) {
            const jsonData = JSON.stringify(jsonResponse, null, 2);
            const blob = new Blob([jsonData], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'schedule_of_notices_of_leases.json';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        }
      };

    return (
        <div className="main-page">
            <h1>Schedule of Notices of Leases PDF Parser</h1>
            {(!isLoading && !isResponse) && <>
                <h2>Please select the pdf you wish to parse</h2>
                <input
                    className='pdf-button'
                    type="file"
                    id="fileInput"
                    onChange={handleFile}
                />
                {file && <>
                    <p>Selected File: {file.name}</p>
                    <button className='go-button' onClick={handleGo}>GO {'\u27BC'}</button>
                </>}
            </>}
            {isLoading &&
                <div className='loader-wrapper'>
                    <Loader type="pacman" style={{transform: 'scale(1.5)'}}/>
                </div>
            }
            {isResponse &&
                <>
                    <div className='json-view'>
                        <JsonView value={jsonResponse} style={vscodeTheme} />
                    </div>
                    <button className='download-button' onClick={handleDownload}>
                        Download JSON
                    </button>
                </>
            }
        </div>
    );
};

export default MainPage;
