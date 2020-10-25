# note: documentation not written yet
# to do: double-check parameter values

# Structure of code and simulation is taken from Jeppe Druehdahl's ASAD-model in NumEcon Repository on GitHub.
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
# prop_cycle = plt.rcParams["axes.prop_cycle"]
# colors = prop_cycle.by_key()["color"]
import ipywidgets as widgets


def simulate(iT=100, deta=0.8, dsigma= 0.8, dbeta=0.0, dalpha=1.0, dphi=0.5, dlambda=0.0, dpstar=0.0, dy_pot=1.0, drstar=0.05, dpi=0.1, iShock=5):

    widgets.interact(
        simulate_,
        deta= widgets.fixed(deta),
        dsigma= widgets.fixed(dsigma),
        dbeta= widgets.fixed(dbeta),
        dalpha= widgets.fixed(dalpha),
        dphi= widgets.fixed(dphi),
        dlambda= widgets.fixed(dlambda),
        dpstar= widgets.fixed(dpstar),
        dy_pot= widgets.fixed(dy_pot),
        drstar= widgets.fixed(drstar),
        dpi= widgets.FloatSlider(
            description="$\\pi$", min=0.01, max=100, step=0.01, value= dpi
        ),
        # iShock= widgets.FloatSlider(
        #     description="Shock period", min=1, max=99, step=1, value= iShock
        # ),
        iShock= widgets.fixed(iShock),
        iT= widgets.fixed(iT),
    )

    # ### a. parameters (values & descriptions)
    # iT=       # time horizon
    # deta=     # income elasticity of demand for money
    # dsigma=   # interest rate semielasticity of demand for money
    # dbeta=    # shift parameter
    # dalpha=   # measures responsiveness of domestic goods demand to changes in RER
    # dphi=     # income elasticity of demand for domestic goods
    # dlambda=  # the interest rate semielasticity of demand for domestic goods
    # dpstar=   # foreign price level, normalized to zero
    # dy_pot=   # natural production level
    # drstar=   # foreign interest rate
    # dpi=      # degree of price flexibility

    # Formed via consistent expectations
    # dtheta=   # speed of adjustment of exchange rate expectations formation

def simulate_(iT, deta, dsigma, dbeta, dalpha, dphi, dlambda, dpstar, dy_pot, drstar, dpi, iShock):
    ### b. steady state and shock
    # iShock=  # time period in which shock happens
    iShock= np.int(iShock)
    vM= np.ones((iT))
    vM[iShock:]= vM[iShock:]*2

    # Green equations
    vP_bar= vM - deta*dy_pot + dsigma*drstar
    vS_bar= vP_bar - dpstar + (1/dalpha)*(dlambda*drstar + (1 - dphi)*dy_pot - dbeta)

    # c. Rate of convergence and consistent expectations coefficient
    dtheta= (dpi*(dlambda/dsigma + dalpha))/2 + (dpi**2*((dlambda/dsigma + dalpha)**2)/4  + (dpi*dalpha)/dsigma)**0.5
    dnu= dpi * (dalpha + (dalpha + dlambda*dtheta)/(dsigma*dtheta))

    ### d. functions

    # Red equations
    p= lambda p_bar, p_0, dnu, t: p_bar + (p_0 - p_bar)*np.exp(-dnu*t)
    s= lambda theta, sigma, p, p_bar, s_bar: s_bar - ( 1/(theta*sigma) )*(p - p_bar)
    r= lambda rstar, theta, s_bar, s: rstar + theta*(s_bar - s)

    ### e. simulation
    # Start from steady state
    vS= np.ones((iT))*vS_bar[0]
    # vS[0]= vS_bar[0]
    vR= np.ones((iT))*drstar
    # vR[0]= drstar
    vP= np.ones((iT))*vP_bar[0]
    # vP[0]= vP_bar[0]



    iPost_shock= 1 # periods since shock
    for t in range(iShock, iT):
        vP[t]= p(vP_bar[t], vP_bar[0], dnu, iPost_shock)
        vS[t]= s(dtheta, dsigma, vP[t], vP_bar[t], vS_bar[t])
        vR[t]= r(drstar, dtheta, vS_bar[t], vS[t])
        iPost_shock = iPost_shock + 1

    # To make a graph with a break, mask the period before the shock, i.e. make it invalid
    mask= np.zeros((iT))
    mask[iShock-1]= 1
    vP_mask= np.ma.masked_array(vP, mask)
    vS_mask= np.ma.masked_array(vS, mask)
    vR_mask= np.ma.masked_array(vR, mask)


    ### e. figure
    fig= plt.figure(figsize=(6,4), dpi=100)
    ax= fig.add_subplot(1,1,1)
    # ax.plot(vP, label= 'Prices', linewidth=2.0)
    ax.plot(vP_mask, label= 'Prices', linewidth=2.0)
    # ax.plot(vR,'--', label= 'Interest rates', linewidth=2.0)
    ax.plot(vR_mask, '--', label= 'Interest rates', linewidth=2.0)
    # ax.plot(vS, label= 'Exchange rate', linewidth=2.0)
    ax.plot(vS_mask, label= 'Exchange rate', linewidth=2.0)
    # ax.plot(vM, '1' ,label= 'Money supply', linewidth=2.0)
    ax.vlines(x=iShock, ymin= vR[iShock] - 0.2, ymax= vS[iShock] + 0.2,colors='k', ls='--', lw=1, label='Money supply shock')

    ax.set_xlabel("time")

    ax.legend(loc='best', fontsize='small')



# simulate()
