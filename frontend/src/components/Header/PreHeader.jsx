import React from 'react';
import Box from "@mui/material/Box";
import {Typography} from "@mui/material";
import {styled} from "@mui/material/styles";

const StyledBox = styled(Box)(() => ({
    display: 'flex',
    justifyContent: 'space-between',
    height: '35px',
    backgroundColor: '#000814',
    color: '#fff',
}));

const PreHeader = () => {
    return (
        <StyledBox>
            <Box>
                <Typography>
                    Telegram, Instagram, Facebook, Discord, Tiktok
                </Typography>
            </Box>
            <Box>
                <Typography>
                    Email: shvab7216@gmail.com
                </Typography>
            </Box>
        </StyledBox>
    );
};

export default PreHeader;