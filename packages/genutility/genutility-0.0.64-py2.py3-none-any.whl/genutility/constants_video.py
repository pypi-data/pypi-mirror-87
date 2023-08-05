from __future__ import absolute_import, division, print_function, unicode_literals

DAR_WS = 16 / 9
DAR_FS = 4 / 3

RES_PAL = (720, 576)
RES_NTSC = (720, 480)
RES_PAL_BLANKING = (704, 576)
RES_NTSC_BLANKING = (704, 480)
RES_PAL_HALF_H = (352, 576)
RES_NTSC_HALF_H = (352, 480)
RES_HALF_HD = (1280, 720)
RES_FULL_HD = (1920, 1080)

PAR_HD = 1

def SAR(RES):
	x, y = RES
	return x / y

# Generic / Digital PAR
PAR_PAL_16_9 = DAR_WS / SAR(RES_PAL) #64:45
PAR_PAL_4_3 = DAR_FS / SAR(RES_PAL) #16:15
PAR_PAL_4_3_BLANKING = DAR_FS / SAR(RES_PAL_BLANKING) #12:11
PAR_PAL_HALF_H = DAR_FS / SAR(RES_PAL_HALF_H) #24:11
PAR_NTSC_16_9 = DAR_WS / SAR(RES_NTSC) #32:27
PAR_NTSC_4_3 = DAR_FS / SAR(RES_NTSC) #8:9
PAR_NTSC_4_3_BLANKING = DAR_FS / SAR(RES_NTSC_BLANKING) #10:11
PAR_NTSC_HALF_H = DAR_FS / SAR(RES_NTSC_HALF_H) #20:11

# MPEG-4 PAR
PAR_MPG4_PAL_16_9 = PAR_PAL_OVERSCAN_16_9 = DAR_WS / SAR(RES_PAL_BLANKING) #16:11
PAR_MPG4_PAL_4_3 = PAR_PAL_OVERSCAN_4_3 = DAR_FS / SAR(RES_PAL_BLANKING) #12:11
PAR_MPG4_NTSC_16_9 = PAR_NTSC_OVERSCAN_16_9 = DAR_WS / SAR(RES_NTSC_BLANKING) #40:33
PAR_MPG4_NTSC_4_3 = PAR_NTSC_OVERSCAN_4_3 = DAR_FS / SAR(RES_NTSC_BLANKING) #10:11

# ITU-R BT.601 PAR (Rec. 601)
PAR_ITU_PAL_16_9 = 512 / 351
PAR_ITU_PAL_4_3 = 128 / 117
PAR_ITU_NTSC_16_9 = 5760 / 4739
PAR_ITU_NTSC_4_3 = 4320 / 4739

# Frames per seconds
REAL_FILM_FPS = 24
NTSC_PROG_FPS = 24000 / 1001
NTSC_VIDEO_FPS = 30000 / 1001
PAL_PROG_FPS = 25
PAL_VIDEO_FPS = 30
